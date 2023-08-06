
from . import util

# TODO(jp): move f-strings with {{arg}} into their respective strings as pure
# f-strings, instead of f-strings created solely to be .format()-ed later.
# More readable that way.

STAGING_SCHEMA = 'mr_plow_staging'
STORE_NAME = f'{STAGING_SCHEMA}.document_store'
TASKS_NAME = f'{STAGING_SCHEMA}.document_tasks'

_CREATE_SCHEMA = f'CREATE SCHEMA IF NOT EXISTS {STAGING_SCHEMA}'

_CREATE_FILE_FORMAT = f"""
CREATE OR REPLACE FILE FORMAT {STAGING_SCHEMA}.{{format_name}}
TYPE = %(format_type)s COMPRESSION = AUTO ;
"""

_CREATE_STAGING = f"""
CREATE OR REPLACE STAGE {STAGING_SCHEMA}.{{stage_name}}
URL = %(s3_bucket_url)s
CREDENTIALS = (AWS_KEY_ID = %(staging_aws_key)s
               AWS_SECRET_KEY = %(staging_aws_secret)s)
FILE_FORMAT = (FORMAT_NAME = {STAGING_SCHEMA}.{{format_name}})
"""

# # schema definitions

# stores outstanding s3 documents ready for ETL
_CREATE_DOCUMENTS = f"""
CREATE TABLE IF NOT EXISTS {STORE_NAME} (
  s3_path VARCHAR PRIMARY KEY,
  source VARCHAR NOT NULL,
  contents VARIANT NOT NULL,
  created_at {util.timestamp_decl}
);
"""

# tracks ETL tasks, one per document per table
_CREATE_TASKS = f"""
CREATE TABLE IF NOT EXISTS {TASKS_NAME} (
  s3_path VARCHAR NOT NULL REFERENCES {STORE_NAME} (s3_path),
  table_name VARCHAR NOT NULL,
  created_at {util.timestamp_decl},
  transformed_at TIMESTAMP_NTZ,
  loaded_at TIMESTAMP_NTZ,
  PRIMARY KEY (s3_path, table_name)
);
"""

_INSERT_DOCUMENT = f"""
COPY INTO {STORE_NAME} (s3_path, source, contents)
FROM (
    SELECT %(s3_path)s, %(source)s, t.$1
    FROM @{STAGING_SCHEMA}.{{stage_name}}/{{s3_key}} t
)
;
"""

# delete document data when no incomplete task is found
_DELETE_DOCUMENTS = f"""
DELETE FROM {STORE_NAME} WHERE s3_path in (
    SELECT s.s3_path
    FROM {STORE_NAME} s
    LEFT OUTER JOIN {TASKS_NAME} t
        ON s.s3_path = t.s3_path AND t.loaded_at IS NULL
    WHERE t.s3_path IS NULL
);
"""

_INSERT_TASK = f"""
INSERT INTO {TASKS_NAME} (s3_path, table_name)
VALUES (%(s3_path)s, %(table_name)s);
"""

# call after doing Table.do_transform(), which draws data from the same filter
_UPDATE_TASKS_TRANSFORMED = f"""
UPDATE {TASKS_NAME}
SET transformed_at = {util.now_ntz}
WHERE transformed_at IS NULL
    AND table_name = '{{t.name}}'
;
"""

# call after doing Table.do_load(), which draws indirectly from the same filter
_UPDATE_TASKS_LOADED = f"""
UPDATE {TASKS_NAME}
SET loaded_at = {util.now_ntz}
WHERE loaded_at IS NULL
    AND transformed_at IS NOT NULL
    AND table_name = '{{t.name}}'
;
"""


# encapsulate queries in functions. Without this, coverage stats are
# meaningless.

def _get_file_format_name(format_type):
    return 'plow_format_' + format_type.lower()


def create_schema(cursor):
    return cursor.execute(_CREATE_SCHEMA)


def create_file_format(cursor, format_type):
    format_name = _get_file_format_name(format_type)
    params = {'format_type': format_type}
    return cursor.execute(_CREATE_FILE_FORMAT.format(format_name=format_name),
                          params)


def create_stage(cursor, stage_name, s3_bucket_url, staging_aws_key,
                 staging_aws_secret, format_type):
    assert stage_name is not None
    params = {
        's3_bucket_url': s3_bucket_url,
        'staging_aws_key': staging_aws_key,
        'staging_aws_secret': staging_aws_secret,
    }
    return cursor.execute(
        _CREATE_STAGING.format(stage_name=stage_name,
                               format_name=_get_file_format_name(format_type)),
        params,
    )


def create_documents(cursor):
    return cursor.execute(_CREATE_DOCUMENTS)


def create_tasks(cursor):
    return cursor.execute(_CREATE_TASKS)


def insert_document(cursor, s3_path, source, stage_name):
    s3_key = s3_path.partition('/')[-1]
    assert s3_key
    params = {'source': source, 's3_path': s3_path}
    return cursor.execute(_INSERT_DOCUMENT.format(stage_name=stage_name,
                                                  s3_key=s3_key), params)


def delete_documents(cursor):
    return cursor.execute(_DELETE_DOCUMENTS)


def insert_tasks(cursor, s3_path, tables):
    if isinstance(tables, (str, bytes)):
        tables = (tables,)
    params = [{'s3_path': s3_path, 'table_name': t} for t in tables]
    return cursor.executemany(_INSERT_TASK, params)


def update_tasks_transformed(cursor, table):
    return cursor.execute(_UPDATE_TASKS_TRANSFORMED.format(t=table))


def update_tasks_loaded(cursor, table):
    return cursor.execute(_UPDATE_TASKS_LOADED.format(t=table))
