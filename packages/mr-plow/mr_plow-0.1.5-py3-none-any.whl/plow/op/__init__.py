"""Enumerates the actual operations being done.

One-time operations:
[staging.py]  create_tables (one-time)
[staging.py]  create_objects (one-time per data format)

Ongoing operations per source:
[s3.py]       extract = call API, persist to S3, trigger next page
[staging.py]  stage = stage from S3 to document_store table

Ongoing operations per table, i.e. after all pages collected
[etl.py]  transform = convert VARIANTs from document_store to staging table
[etl.py]  load = dedupe/upsert to main table, and clear rows from staging table
"""


from . import etl, extract, staging  # noqa: F401
from .etl import create_table, transform, load  # noqa: F401
from .extract import Extractor  # noqa: F401
from .staging import (  # noqa: F401
    create_schema, create_documents, create_tasks, create_tables,
    create_file_format, create_stage, create_objects,
    stage_document,
)
