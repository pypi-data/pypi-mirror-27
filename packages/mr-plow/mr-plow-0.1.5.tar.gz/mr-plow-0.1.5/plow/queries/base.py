"""Common logic for per-vendor ETL"""
from importlib import import_module
import re

from . import etl_tracking
from . import util


def export(tables):
    def decorator(cls):
        instance = cls()
        tables[instance.name] = instance
        return cls
    return decorator


def tables_for(source):
    module = import_module('..' + source, __name__)
    return module.tables


_missing = object()


class optional_property:
    def __init__(self, f):
        self._f = f
        self.__doc__ = f'<{self.__class__.__name__.upper()}> {f.__doc__}'
        self.__name__ = f.__name__

    def __set_name__(self, owner, name):
        self.__objclass__ = owner
        self.__attr_name = f'_{owner.__name__}_prop_{name}'

    def _default(self, obj):
        return self._f(obj)

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        val = getattr(obj, self.__attr_name, _missing)
        if val is _missing:
            return self._default(obj)
        return val

    def __set__(self, obj, value):
        setattr(obj, self.__attr_name, value)


class required_property(optional_property):
    def _default(self, _):
        raise AttributeError(f'attribute {self.__name__!r} not set')


class Table(object):
    f"""Base class to store common SQL logic.

    Much of the logic is similar across all the tables we are persisting to.
    Classes need only specify a name and column declarations for their table,
    a SELECT statement for how to extract data from a JSON object, and which
    columns should be considered unique when merging in new data.

    We also support constraints (though except for NOT NULL Snowflake does not
    enforce them), and procedures for updating an existing row.

    The table is implemented in snowflake by creating two tables. The first,
    the "staging" table, is a target for the transformed data. The second, the
    "main" table, is the target for the same data after it has been filtered
    for duplicate keys.

    To implement tables for a given source, create a dedicated module for them.
    Create a base class and give it a sensible "source" attribute (this is
    used to organize the tables and is usually the same as the name of the
    module). Subclass for each desired table, and implement properties as
    needed.

    Attributes marked as "required_property" must be specified in order to
    use an instance. Attributes marked as "optional_property" have meaningful
    defaults but may be useful to specify. For both, specify by setting the
    variable in the class body, setting the attribute directly (e.g. in
    __init__, or as in unit tests after creation), or by defining as a class
    @property.
    """

    # attributes that are usually overridden.

    @required_property
    def name(self):
        """A canonical name for this table.

        Must be a valid SQL table identifier without periods.
        """

    @required_property
    def source(self):
        """A name for the "category" this table belongs to.

        This generally means the vendor supplying its information. Usually set
        in a base class.

        By default this is used as a schema name, so unless the "schema"
        attribute is overridden, "source" must a valid SQL identifier.
        """

    @required_property
    def column_spec(self):
        """A list of pairs (column_name, type_and_constraint).

        Note that Mr. Plow automatically adds several columns for tracking
        purposes; see full_column_spec() for details.
        """

    @optional_property
    def constraints(self):
        """Specifies constraints on a table, e.g. a composite primary key.

        Note that Snowflake enforces very few constraints; these are provided
        mostly as a declaration of intention and structure.

        Given as a sequence or generator of string pairs, like column_spec,
        except that the first must be empty.
        """
        return ()

    @required_property
    def select(self):
        """A select statement to populate the "staging" table from raw data.

        Usually this will be something like:

            f'''SELECT
                    (JSON manipulations)
                FROM {self.from_clause}
                WHERE {self.where_clause} [AND (other WHERE conditions)]
            '''

        where the user is responsible for populating the JSON manipulations.
        """

    @optional_property
    def merge_join(self):
        """Column names considered unique for merge purposes.

        By default, primary keys.
        """
        return self.primary_keys()

    @optional_property
    def merge_updates(self):
        """Columns to update if a row in the staging table matches an existing
        row in the main table.

        Given as a list of pairs (column_name, update_expression). The update
        expression should reference only self.tablename and
        self.merge_source_name.

        See the .compare_* methods to simplify construction of complex update
        expressions.

        ::note
        This should, semantically, reflect API data you expect to change if it
        is encountered twice in different API extractions. It should not
        include the following:
            * any keys given in merge_join
            * "created_at" (this should logically stay the same)
            * "s3_path" (automatically updated by Mr. Plow)
            * "merged_at" (automatically set by Mr. Plow to CURRENT_TIMESTAMP)
        """
        return ()

    @optional_property
    def from_clause(self):
        """FROM clause to be used when populating staging table.

        Queries the staging.DOCUMENT_STORE table for raw JSON data.

        This is often overridden by a base class, e.g. to add a FLATTEN from a
        JSON array. If you do, the superclass result must be used or joined.
        """
        return f"""
            {etl_tracking.STORE_NAME} t
            JOIN {etl_tracking.TASKS_NAME} tasks
                ON t.s3_path = tasks.s3_path
        """

    @optional_property
    def where_clause(self):
        """WHERE clause to be used when populating staging table

        Filters on the staging.TASKS_STORE table to select JSON data that has
        not yet been transformed.

        Subclasses overriding this must provide the superclass result in an
        AND clause.
        """
        return f"""
            t.source = '{self.source}'
            AND tasks.table_name = '{self.name}'
            AND tasks.transformed_at IS NULL
        """

    @optional_property
    def schema(self):
        """The schema for the "main" table; usually named after the source.

        If overridden for any reason, it should be done in a base class.
        """
        return self.source

    @optional_property
    def merge_source_view(self):
        """Deduping view.

        Implement as a CREATE VIEW to dedupe records if the table's primary
        keys may appear twice in the staging table.

        The name should match merge_source_name.
        """
        return None

    @optional_property
    def merge_source_name(self):
        """The name of the deduping view given in merge_source_view.

        By default this just points to the staging table.

        This name should be schema-qualified, and ideally should be in
        etl_tracking.STAGING_SCHEMA.
        """
        return self.staging_tablename

    # methods and helpers to provide basic information about the table

    _pk_patt = re.compile(r'PRIMARY\s+KEY\s*(?:\((\w+(?:\s*,\s*\w+)*\w*)\))?',
                          re.IGNORECASE)

    @property
    def _constraint_spec(self):
        constr = self.constraints
        if not constr:
            constr = ()
        if isinstance(constr, str):
            constr = (constr,)
        return (('', c) for c in constr)

    def primary_keys(self):
        """Extracts primary key information from column description"""
        pk = None
        for col, desc in (*self.full_column_spec(None),
                          *self._constraint_spec):
            match = self._pk_patt.search(desc)
            if match:
                if pk is not None:
                    raise ValueError(f'Table {self.name} has two primary keys')
                pk = (col,) if col else \
                    tuple(match.group(1).replace(',', ' ').split())
        return pk

    def _unique_columns(self):
        """used for testing; lists keys to be used for uniqueness testing.

        Given in lowercase form since snowflake erases cases and the tests, by
        convention, lowercase the uppercased keys.
        """
        return [x.lower()
                for x in (*self.primary_keys(),
                          *getattr(self, 'uniqueness_tiebreakers', ()))]

    def _tablename(self, is_main, *, name=None):
        """Generate a schema-qualified table name.

        :param is_main: if true, primary table; otherwise, the staging copy.
        :param name: optional table name. Omit and we use this table's name.
        """
        if name is None:
            name = self.name
        if is_main:
            return f'{self.schema}.{name}'
        else:
            return f'{etl_tracking.STAGING_SCHEMA}.{self.schema}_{name}'

    @property
    def tablename(self):
        """Schema-qualified name for the table. Use this in SQL statements.

        Do not override.
        """
        return self._tablename(True)

    @property
    def staging_tablename(self):
        """Schema-qualified name for the staging table.

        Do not override.
        """
        return self._tablename(False)

    @staticmethod
    def parenthify(items):
        """Parenthesized, comma-joined string

        :param items: an iterable of str objects
        """
        items = ", ".join(items)
        return f'({items})'

    _reference_patt = re.compile(r'(?<=REFERENCES )(\w+)(?=\s+\(\w+\))', re.I)

    def full_column_spec(self, main):
        """full list of columns/types.

        :param main:
            if True, treat as column spec for main table. (include S3
                filename, record-creation timestamp, and record-modification
                timestamp)
            if False, treat as column spec for staging table. (include S3
                filename and record-creation timestamp)
            if None, treat as columns that must be populated by an INSERT
                statement. (include S3 filename)
        """

        for colname, colspec in self.column_spec:
            replstr = self._tablename(main, name=r'\1')
            # i.e. "livechat.\1" or "{STAGING_SCHEMA}.livechat_\1"; the "\1"
            # is then used by regex.sub() to substitute the detected tablename
            colspec = self._reference_patt.sub(replstr, colspec)
            yield colname, colspec

        # extra columns
        yield 's3_path', 'VARCHAR NOT NULL'
        if main is not None:
            if main:
                yield 'created_at', 'TIMESTAMP_NTZ NOT NULL'
                yield 'merged_at', util.timestamp_decl
            else:
                yield 'created_at', util.timestamp_decl

    def table_spec(self, which):
        """Generate the parenthesized part of a CREATE TABLE statement.

        :param which: passed to full_column_spec()
        """
        specs = list(self.full_column_spec(which))
        specs.extend(self._constraint_spec)
        return self.parenthify(map(' '.join, specs))

    def columns(self, main):
        """String listing column names in parenthesis. Can be used for INSERTs.

        :param main: passed directly to full_column_spec.
        """
        return self.parenthify(c for c, t in self.full_column_spec(main))

    def do_create(self, cursor):
        """Execute SQL to create the objects required for this table."""
        cursor.execute(self.create_schema())
        cursor.execute(self.create())
        cursor.execute(self.create_staging())
        merge_source = self.merge_source_view
        if merge_source is not None:
            cursor.execute(merge_source)

    def do_transform(self, cursor):
        """Execute SQL to carry out transformation from raw data to staging
        table."""
        cursor.execute(self.transform())
        etl_tracking.update_tasks_transformed(cursor, self)

    def do_merge(self, cursor):
        """Execute SQL to dedupe data from staging table to main table."""
        cursor.execute(self.merge())
        etl_tracking.update_tasks_loaded(cursor, self)
        cursor.execute(self.delete_staging())

    def create_schema(self):
        """SQL command to conditionally create main schema for this table."""
        return f'CREATE SCHEMA IF NOT EXISTS {self.schema};'

    def _create_table(self, main):
        """SQL command to CREATE TABLE.

        :param main: passed to full_column_spec()
        """
        table = self.tablename if main else self.staging_tablename
        spec = self.table_spec(main)
        return f'CREATE TABLE IF NOT EXISTS {table} {spec};'

    def create(self):
        """SQL command to CREATE main table."""
        return self._create_table(True)

    def create_staging(self):
        """SQL command to create staging table."""
        return self._create_table(False)

    def transform(self):
        """SQL command to populate staging table from raw data."""
        columns = self.columns(None)
        select = self.select()
        return f'INSERT INTO {self.staging_tablename} {columns} {select}'

    def _merge_conditions(self, table, *extras):
        """SQL boolean clause for joining staging to main table.

        see merge_join.

        Subclasses that override this method MUST include the superclass
        implementation.

        :param table: the table or view to join the main table against
        :param *extras: any other SQL conditions to add to the AND clause.
        """
        return ' AND '.join((*(f'{self.tablename}.{col} = {table}.{col}'
                               for col in self.merge_join),
                             *extras))

    def updatable(self):
        """Generates update instructions as string pairs (target, value)"""
        updates = list(self.merge_updates or ())
        assert all(c not in ('s3_path', 'merged_at', 'created_at')
                   for c, v in updates)
        yield from updates
        if updates:
            yield 's3_path', f'{self.merge_source_name}.s3_path'
        yield 'merged_at', util.now_ntz

    def merge(self):
        """SQL statement to dedupe data from staging table to main table."""
        updates = ', '.join(map(' = '.join, self.updatable()))
        columns = self.columns(False)
        conds = self._merge_conditions(self.merge_source_name)
        return f"""
            MERGE INTO {self.tablename}
            USING {self.merge_source_name} ON {conds}
            WHEN MATCHED THEN UPDATE SET {updates}
            WHEN NOT MATCHED THEN INSERT {columns} VALUES {columns}
        """

    def delete_staging(self):
        """SQL command to clear merged data out of the staging table."""
        conds = self._merge_conditions(
            self.staging_tablename,
            (f'{self.tablename}.merged_at'
             f' > {self.staging_tablename}.created_at')
        )
        return f"""
            DELETE FROM {self.staging_tablename} USING {self.tablename}
            WHERE {conds}
        """

    # some functions to aid building complicated merge updates

    def _update_all(self):
        """Use to have a table update all attributes on merges

        example:

            class MyTable(Table):
                ...
                merge_updates = property(Table._update_all)
        """
        return [(c, self.compare_new('coalesce', c))
                for c, t in self.column_spec if c not in self.merge_join]

    def compare_new(self, comparator, attr):
        """SQL expression to apply a function to staging then main columns.

        e.g. tbl.compare_new('coalesce', 'mycolumn') returns
        "coalesce(staging.mycolumn, main.mycolumn)", which is the value from
        the staging table, falling back to that of the main table if it is
        null. Use to let the new version override the old if it is given.
        """
        return f'''
            {comparator}({self.merge_source_name}.{attr},
                         {self.tablename}.{attr})
        '''

    def compare_old(self, comparator, attr):
        """SQL expression to apply a function to main then staging columns.

        e.g. tbl.compare_old('coalesce', 'mycolumn') returns
        "coalesce(main.mycolumn, staging.mycolumn)", which is the value from
        the main table, falling back to that of the staging table if it is
        null. Use to prefer the old version unless it is null.
        """
        return f'''
            {comparator}({self.tablename}.{attr},
                         {self.merge_source_name}.{attr})
        '''

    def compare_coalesce(self, comparator, attr, default):
        """Like "compare_new" but resolves null values to a default before
        applying the operation.

        The default must be a valid SQL expression, it is used in the string
        without escapes. Therefore to supply a string value, it must be quoted.

        E.g. tbl.compare_coalesce('greatest', 'duration', '0') expresses the
        larger of staging.duration and main.duration, substituting 0 if either
        of them is null.
        """
        return f'''
            {comparator}(
                coalesce({self.merge_source_name}.{attr}, {default}),
                coalesce({self.tablename}.{attr}, {default})
            )
        '''
