import functools

from .base import get_config
from ..queries import etl_tracking as q


def _cursor_optional(*reqd_config):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*, config, cursor=None, **kwargs):
            if cursor is None:
                config = get_config(config, *reqd_config)
                cursor = config.snowflake().cursor()
            return f(cursor=cursor, config=config, **kwargs)
        return wrapped
    return wrapper


@_cursor_optional()
def create_schema(*, cursor, **kwargs):
        q.create_schema(cursor)


@_cursor_optional()
def create_documents(*, cursor, **kwargs):
    q.create_documents(cursor)


@_cursor_optional()
def create_tasks(*, cursor, **kwargs):
    q.create_tasks(cursor)


@_cursor_optional()
def create_tables(*, cursor, config, **kwargs):
    """Should be run at least once for any Snowflake database."""
    create_schema(cursor=cursor, config=config)
    create_documents(cursor=cursor, config=config)
    create_tasks(cursor=cursor, config=config)


def _create_staging_objects(f):
    @_cursor_optional('plow_s3_bucket', 'staging_s3_access_key_id',
                      'staging_s3_secret_access_key')
    @functools.wraps(f)
    def wrapped(*, cursor, stage_name=None, format_type=None, **kwargs):
        if stage_name is None:
            if format_type is None:
                raise ValueError('must specify format_type and/or stage_name')
            stage_name = f'plow_stage_{format_type}'
        return f(cursor=cursor, stage_name=stage_name, format_type=format_type,
                 **kwargs)
    return wrapped


@_create_staging_objects
def create_file_format(*, cursor, format_type, **kwargs):
    q.create_file_format(cursor, format_type)


@_create_staging_objects
def create_stage(*, cursor, stage_name, format_type, config):
    q.create_stage(
        cursor,
        stage_name=stage_name,
        s3_bucket_url='s3://' + config.plow_s3_bucket,
        staging_aws_key=config.staging_aws_access_key_id,
        staging_aws_secret=config.staging_aws_secret_access_key,
        format_type=format_type,
    )


@_create_staging_objects
def create_objects(*, cursor, stage_name, format_type, config):
    create_schema(cursor=cursor, config=config)
    create_file_format(cursor=cursor, format_type=format_type, config=config)
    create_stage(cursor=cursor, stage_name=stage_name, format_type=format_type,
                 config=config)


@_cursor_optional('plow_s3_bucket')
def stage_document(*, cursor, s3_key, stage_name, config, tables, source=None):
    """Store a given S3 document and set up tracking for it.

    Specifically inserts the document content into the document store and
    stores task entries for the document and the given tables to the tasks
    table.

    :param cursor: an optional Snowflake cursor
    :param s3_key: the key of the s3 document to be stored
    :param stage_name: the Snowflake "stage" to draw the document from (see
        create_stage())
    :param config: a Config object
    :param tables: a list of string table names for which to store tasks
        entries for the document
    :param source: a string to give as the data's "source" in the documents
        table. If absent it is taken from the config; if absent there too, a
        ValueError is thrown.
    """
    if source is None:
        if config.plow_data_source is None:
            raise ValueError('data source needed to stage a document!')
        source = config.plow_data_source
    s3_path = f'{config.plow_s3_bucket}/{s3_key}'

    cursor.execute('BEGIN')
    try:
        q.insert_tasks(cursor, s3_path=s3_path, tables=tables)
        # that should be reasonably quick; inserting actual data could take
        # longer
        q.insert_document(cursor, s3_path=s3_path, source=source,
                          stage_name=stage_name)
    except Exception:
        cursor.execute('ROLLBACK')
        raise
    else:
        cursor.execute('COMMIT')
