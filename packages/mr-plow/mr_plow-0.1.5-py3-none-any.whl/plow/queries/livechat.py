"""Stores the SQL statements for Livechat."""
from collections import OrderedDict

from .base import export, Table as BaseTable
from .etl_tracking import STAGING_SCHEMA

tables = OrderedDict()


class Table(BaseTable):
    source = 'livechat'

    @property
    def from_clause(self):
        return "{}, LATERAL FLATTEN(INPUT => t.contents:chats) chats".format(
            super().from_clause)


@export(tables)
class Visitors(Table):
    name = 'visitors'
    column_spec = (
        ('visitor_id', 'VARCHAR PRIMARY KEY'),
        ('city', 'VARCHAR'),
        ('country', 'VARCHAR'),
        ('country_code', 'VARCHAR'),
        ('name', 'VARCHAR'),
        ('region', 'VARCHAR'),
        ('timezone', 'VARCHAR'),
        ('ip', 'VARCHAR'),
        ('_chat_started', 'TIMESTAMP_NTZ'),
    )

    merge_join = ('visitor_id',)

    def select(self):
        return f"""
            SELECT
                NULLIF(STRIP_NULL_VALUE(chats.value:visitor_id), ''),
                STRIP_NULL_VALUE(chats.value:visitor:city),
                STRIP_NULL_VALUE(chats.value:visitor:country),
                STRIP_NULL_VALUE(chats.value:visitor:country_code),
                STRIP_NULL_VALUE(chats.value:visitor:name),
                STRIP_NULL_VALUE(chats.value:visitor:region),
                STRIP_NULL_VALUE(chats.value:visitor:timezone),
                STRIP_NULL_VALUE(chats.value:visitor:ip),
                TO_TIMESTAMP_NTZ(
                    STRIP_NULL_VALUE(chats.value:started_timestamp)::integer),
                t.s3_path
            FROM
                {self.from_clause}
            WHERE
                {self.where_clause}
                AND NOT (IS_NULL_VALUE(chats.value:visitor)
                         OR IS_NULL_VALUE(chats.value:visitor_id))
        """

    @property
    def merge_updates(self):
        src = self.merge_source_name
        tbl = self.tablename
        return [
            (col, (f'CASE WHEN {src}._chat_started > {tbl}._chat_started'
                   f' THEN {src}.{col} ELSE {tbl}.{col} END'))
            for col, _ in self.column_spec if col != 'visitor_id'
        ]

    merge_source_name = f'{STAGING_SCHEMA}.livechat_visitors_dedupe'

    @property
    def merge_source_view(self):
        cols = self.columns(False)
        window = (
            'IGNORE NULLS OVER ('
            ' PARTITION BY visitor_id'
            ' ORDER BY _chat_started DESC)'
        )
        return f"""
            CREATE OR REPLACE VIEW {self.merge_source_name} {cols} AS
            SELECT DISTINCT
                v.visitor_id,
                FIRST_VALUE(v.city) {window},
                FIRST_VALUE(v.country) {window},
                FIRST_VALUE(v.country_code) {window},
                FIRST_VALUE(v.name) {window},
                FIRST_VALUE(v.region) {window},
                FIRST_VALUE(v.timezone) {window},
                FIRST_VALUE(v.ip) {window},
                FIRST_VALUE(v._chat_started) {window},
                FIRST_VALUE(v.s3_path) {window},
                FIRST_VALUE(v.created_at) {window}
            FROM
                {self.staging_tablename} v
        """


@export(tables)
class Chats(Table):
    name = 'chats'
    column_spec = (
        ('chat_id', 'VARCHAR PRIMARY KEY'),
        ('duration', 'NUMBER(11, 2)'),
        ('chat_start_url', 'VARCHAR'),
        ('source', 'VARCHAR'),
        ('kenshoo_id', 'VARCHAR'),
        ('return_customer', 'BOOLEAN'),
        ('product_intent', 'VARCHAR'),
        ('direct_shopping', 'BOOLEAN'),
        ('started_timestamp', 'TIMESTAMP_NTZ NOT NULL'),
        ('ended_timestamp', 'TIMESTAMP_NTZ'),
        ('engagement', 'VARCHAR'),
        ('rate', 'VARCHAR'),
        ('referrer', 'VARCHAR'),
        ('timezone', 'VARCHAR'),
        ('is_pending', 'BOOLEAN'),
        ('visitor_id', 'VARCHAR REFERENCES visitors (visitor_id)'),
    )

    merge_join = ('chat_id',)

    @property
    def merge_updates(self):
        def greatest(attr, default):
            return (attr, self.compare_coalesce('greatest', attr, default))

        return (
            greatest('ended_timestamp', '0::timestamp_ntz'),
            greatest('duration', '0'),
            ('rate', self.compare_new('coalesce', 'rate')),
        )

    def select(self):
        # note: this makes use of the "flatten_custom_vars" user-defined
        # function. This is defined in the overridden "do_create()" method.
        custom_vars = f'{self.flatten_function}(chats.value:custom_variables)'
        return f"""
            SELECT
                NULLIF(STRIP_NULL_VALUE(chats.value:id), '') AS chat_id,
                STRIP_NULL_VALUE(chats.value:duration),
                STRIP_NULL_VALUE(chats.value:chat_start_url),
                TRIM(STRIP_NULL_VALUE({custom_vars}:source)),
                TRIM(STRIP_NULL_VALUE({custom_vars}:kenshoo_id)),
                STRIP_NULL_VALUE({custom_vars}:return_customer),
                TRIM(STRIP_NULL_VALUE({custom_vars}:product_intent)),
                STRIP_NULL_VALUE({custom_vars}:direct_shopping),
                TO_TIMESTAMP_NTZ(
                    STRIP_NULL_VALUE(chats.value:started_timestamp)::integer),
                TO_TIMESTAMP_NTZ(
                    STRIP_NULL_VALUE(chats.value:ended_timestamp)::integer),
                STRIP_NULL_VALUE(chats.value:engagement),
                STRIP_NULL_VALUE(chats.value:rate),
                STRIP_NULL_VALUE(chats.value:referrer),
                STRIP_NULL_VALUE(chats.value:timezone),
                COALESCE(STRIP_NULL_VALUE(chats.value:pending), false),
                STRIP_NULL_VALUE(chats.value:visitor_id),
                t.s3_path
            FROM
                {self.from_clause}
            WHERE
                {self.where_clause}
        """

    # turns [{key: "foo", value: "bar"}] into {foo: "bar"}
    flatten_function_code = """
        var obj = {};
        CUSTOM_DATA.forEach((item) => {
            var key = item.key;
            if (!key) {
              throw "Could not convert " + JSON.stringify(CUSTOM_DATA);
            }
            var value = item.value || null;
            if (value === "undefined") {
              value = null;
            }
            obj[item.key.toLowerCase().replace(/ /g, "_")] = value;
        });
        return obj;
    """
    flatten_function = f'{STAGING_SCHEMA}.flatten_custom_vars'
    create_flatten_function = f"""
    CREATE OR REPLACE FUNCTION {flatten_function}(CUSTOM_DATA ARRAY)
        RETURNS OBJECT
        LANGUAGE JAVASCRIPT
        STRICT IMMUTABLE
        AS '{flatten_function_code}'
    """

    def do_create(self, cursor):
        cursor.execute(self.create_flatten_function)
        return super().do_create(cursor)


@export(tables)
class Agents(Table):
    name = 'agent_interactions'
    column_spec = (
        ('chat_id', 'VARCHAR NOT NULL REFERENCES chats (chat_id)'),
        ('email', 'VARCHAR NOT NULL'),
        ('display_name', 'VARCHAR'),
        ('ip', 'VARCHAR')
    )
    constraints = 'PRIMARY KEY (chat_id, email)'

    merge_join = ('chat_id', 'email')
    merge_updates = property(BaseTable._update_all)

    def select(self):
        return f"""
            SELECT
                NULLIF(STRIP_NULL_VALUE(chats.value:id), ''),
                NULLIF(STRIP_NULL_VALUE(agents.value:email), ''),
                STRIP_NULL_VALUE(agents.value:display_name),
                STRIP_NULL_VALUE(agents.value:ip),
                t.s3_path
            FROM
                {self.from_clause},
                LATERAL FLATTEN(INPUT => chats.value:agents) agents
            WHERE
                {self.where_clause}
                AND NOT (IS_NULL_VALUE(agents.value)
                         OR IS_NULL_VALUE(agents.value:email))
        """


@export(tables)
class Events(Table):
    name = 'events'
    column_spec = (
        ('chat_id', 'VARCHAR NOT NULL REFERENCES chats (chat_id)'),
        ('index', 'INTEGER NOT NULL'),
        ('agent_id', 'VARCHAR'),
        ('text', 'VARCHAR'),
        ('timestamp', 'TIMESTAMP_NTZ NOT NULL'),
        ('type', 'VARCHAR NOT NULL'),
        ('user_type', 'VARCHAR NOT NULL'),
        ('is_welcome_message', 'BOOLEAN NOT NULL'),
    )
    constraints = 'PRIMARY KEY (chat_id, index)'

    merge_join = ('chat_id', 'index')

    def select(self):
        return f"""
            SELECT
              NULLIF(STRIP_NULL_VALUE(chats.value:id), ''),
              events.index,
              STRIP_NULL_VALUE(events.value:agent_id),
              STRIP_NULL_VALUE(events.value:text),
              TO_TIMESTAMP_NTZ(STRIP_NULL_VALUE(events.value:timestamp)::integer), --# noqa
              NULLIF(STRIP_NULL_VALUE(events.value:type), ''),
              NULLIF(STRIP_NULL_VALUE(events.value:user_type), ''),
              COALESCE(STRIP_NULL_VALUE(events.value:welcome_message), false),
              t.s3_path
            FROM
              {self.from_clause},
              LATERAL FLATTEN(INPUT => chats.value, PATH => 'events') events
            WHERE
                {self.where_clause}
        """


@export(tables)
class Tags(Table):
    name = 'chat_tags'
    column_spec = (
        ('chat_id', 'VARCHAR NOT NULL'),
        ('tag', 'VARCHAR NOT NULL'),
    )
    constraints = 'PRIMARY KEY (chat_id, tag)'

    merge_join = ('chat_id', 'tag')

    def select(self):
        return f"""
            SELECT
                NULLIF(STRIP_NULL_VALUE(chats.value:id), ''),
                NULLIF(STRIP_NULL_VALUE(tags.value), ''),
                t.s3_path
            FROM
                {self.from_clause},
                LATERAL FLATTEN(INPUT => chats.value, PATH => 'tags') tags
            WHERE
                {self.where_clause}
        """
