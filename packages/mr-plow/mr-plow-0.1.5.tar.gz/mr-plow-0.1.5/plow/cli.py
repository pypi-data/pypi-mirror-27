"""CLI for Mr. Plow.

Order of operation:

\b
Do these only when setting up your snowflake DB:
* plow setup-docs
* plow setup-stage

\b
Do these once per data load:
* plow extract [options]
* plow stage [options] S3_OUPUT_PATH_1 S3_OUTPUT_PATH_2 ...
### Try this to do both: ###
* plow extract [options] | xargs plow stage [options]

\b
Do these for each table:
* plow create-tables [options] TABLES...
* plow transform [options] TABLES...
* plow load [options] TABLES...

You can use "ALL" instead of naming the individual tables.

Mr. Plow includes two built-in data sources: livechat and snapfulfil. To write
your own, implement your own `plow.op.Extractor` and `plow.query.Table`s, and
create a `plow.cli.Source` to point to them. See the --source option on the
`extract`, `stage`, `transform`, or `load` commands for more detail.
"""
import code
from collections import namedtuple
from datetime import datetime
from functools import wraps
from importlib import import_module
import json
import os.path
import sys

import click

from .config import Config
from . import op
from .queries import etl_tracking as q


def _add_doc(f, doc=__doc__):
    f.__doc__ = doc
    return f


def get_config(ctx, param, value):
    config = Config.from_filename(value)
    ctx.obj['config'] = config
    return config


@click.group(help=__doc__)
@click.option('-c', '--config', callback=get_config, envvar='MR_PLOW_CONFIG',
              required=True, help='.ini, .json, or .yaml config file.')
@_add_doc
def cli(config):
    pass


cli.__doc__ = __doc__


class Source(namedtuple('Source', 'source tables extractor')):
    """Use a Source to tell the Mr. Plow CLI how to extract and transform data.

    You may provide anything, not just this Source type, as long as it has
    these attributes:

    :param source: string used as `source` for tracking purposes in db
    :param tables: a dict mapping Table.name to Table instance.
    :param extractor: an Extractor instance
    """
    pass


def make_source(ctx, param, value):
    if not value:
        config = ctx.obj['config']
        module = config.plow_source_module
        name = config.plow_source_object
        if not (module and name):
            raise click.BadParameter('You must provide --source, or'
                                     ' specify "plow_source_module" and'
                                     ' "plow_source_object" in config.')
    else:
        if ':' not in value:
            value = f'plow.vendors.{value}:source'
        module, colon, name = value.partition(':')
        if not (module and colon and name):
            raise click.BadParameter('must be of the form <module>:<source>')
    return getattr(import_module(module), name)


source_option_decorator = click.option(
    '-s', '--source', callback=make_source,
    help=('Data source to use. Use one of the provided ones -- currently'
          ' "livechat" and "snapfulfil" -- or provide "<module>:<source>" to'
          ' name a module and a Source object defined in that module. See'
          ' plow.cli.Source docs for more info. You may alternatively specify'
          ' this using "plow_source_module" and "plow_source_object" in'
          ' config.')
)

bucket_option = click.option('-b', '--s3-bucket', envvar='PLOW_S3_BUCKET',
                             default='poppin-mr-plow-test',
                             help='S3 bucket to store data to.')
stage_option = click.option('-t', '--stage-name',
                            help='Name of a Snowflake stage.')


format_option = click.option(
    '--format-type', default='JSON',
    help=("FORMAT_TYPE parameter for Snowflake's CREATE FILE FORMAT"
          " command. At present we only support JSON, which is the"
          " default."))


def use_config(f):
    @click.pass_context
    @wraps(f)
    def wrapped(ctx, **kwargs):
        config = Config(ctx.obj['config'])
        if 's3_bucket' in kwargs:
            config.plow_s3_bucket = kwargs.pop('s3_bucket')
        if 'source' in kwargs:
            config.plow_data_source = kwargs['source'].source
        return f(cfg=config, **kwargs)
    return wrapped


@cli.command(name='setup-docs')
@use_config
def setup_docs(cfg, **kwargs):
    """Create housekeeping tables for ETL ops.

    This should be done at least once before running ETL operations.
    """
    cursor = cfg.snowflake().cursor()
    click.echo(f'creating staging schema {q.STAGING_SCHEMA}', nl=False)
    op.create_schema(config=cfg, cursor=cursor)
    click.echo(f'\ncreating {q.STORE_NAME} table...', nl=False)
    op.create_documents(config=cfg, cursor=cursor)
    click.echo(f'\ncreating {q.TASKS_NAME} table...', nl=False)
    op.create_tasks(config=cfg, cursor=cursor)
    click.echo('\nDone!')


@cli.command(name='setup-stage')
@bucket_option
@stage_option
@format_option
@use_config
def setup_stage(cfg, stage_name, format_type, **kwargs):
    """Create FILE FORMAT and STAGE objects.

    This should be done at least once before running ETL operations.
    """
    format_type = format_type.upper()
    cursor = cfg.snowflake().cursor()
    click.echo(f'Creating staging schema {q.STAGING_SCHEMA}...', nl=False)
    op.create_schema(config=cfg, cursor=cursor)
    click.echo(f'\nCreating file format for {format_type!r}...', nl=False)
    op.create_file_format(config=cfg, cursor=cursor, format_type=format_type)
    click.echo(f'\nCreating Snowflake STAGE {stage_name!r}...', nl=False)
    op.create_stage(config=cfg, cursor=cursor, stage_name=stage_name,
                    format_type=format_type)
    click.echo('\nDone!')


def dict_part(ctx, param, values):
    retval = {}
    for value in values:
        k, eq, v = value.partition('=')
        if not eq:
            raise click.BadParameter('must be given as key=value')
        retval[k] = v
    return retval


@cli.command()
@click.option('-q', '--query-param', callback=dict_part, multiple=True,
              help=('API query parameters to add to the url. Specified as'
                    ' key=value. Can be given several times, though currently'
                    ' giving the same key several times is not supported.'))
@click.option('--follow-up', type=int, default=0,
              help=('Number of follow-up API calls to do after the first one.'
                    ' Zero by default. Negative input means unlimited calls'
                    ' till all available data is fetched.'))
@click.option('-u', '--url',
              help='Override the usual API url for the given source.')
@click.option('-k', '--s3-key',
              help=('Template for S3 keys per "page" of data. For livechat,'
                    ' should include "{page}" where you want the page number'
                    ' to appear. For Snap, use "{$skip}" (be careful with'
                    ' shell escapes) and any other query params.'))
@bucket_option
@click.option('--quiet/--no-quiet', default=False,
              help='suppress verbose output')
@source_option_decorator
@use_config
def extract(cfg, source, query_param, follow_up, url, s3_key, quiet):
    """Access a source API and store data to S3.

    It prints a list to stdout of the S3 keys created. These may be
    investigated using your favorite means of accessing S3. Keep in mind that
    all content is compressed using gzip. Example:

    \b
    $ aws s3 cp s3://my-bucket/my-s3-key - | gunzip -c
    {"spam": "eggs"}

    They may also be piped to another command, e.g. xargs plow stage:

    \b
    $ plow extract [options] | xargs plow stage [options]

    Logging information is printed to stderr.
    """
    if s3_key is None:
        s3_key = _get_default_key_format(source)

    params = dict(query_param or {})

    def make_s3_key(**kwargs):
        _params = kwargs.get('params', {})
        if source.source == 'snapfulfil':
            _params.setdefault('$skip', 0)
        elif source.source == 'livechat':
            _params.setdefault('page', 1)
        return s3_key.format(**_params)

    if follow_up < 0:
        iterations = None
    else:
        iterations = follow_up + 1
    get_data_args = {'params': params}
    if url is not None:
        get_data_args['url'] = url
    new_args = source.extractor.iterative_extract(
        config=cfg,
        make_s3_key=make_s3_key,
        iterations=iterations,
        verbose=not quiet,
        filename_callback=click.echo,
        **get_data_args
    )
    if new_args is not None:
        click.echo('follow-up suggestions: ', nl=False, file=sys.stderr)
        click.echo(json.dumps(new_args, indent=2),
                   file=sys.stderr)
    click.echo('Done! Now do "stage" on those s3 docs', file=sys.stderr)


@cli.command()
@bucket_option
@stage_option
@format_option
@source_option_decorator
@click.argument('s3_files', nargs=-1)
@use_config
def stage(cfg, stage_name, s3_files, format_type, source, **kwargs):
    """Transfer data from S3 to Snowflake.

    Do this for each s3 file printed by the "extract" command.
    """
    cursor = cfg.snowflake().cursor()
    if not stage_name:
        if not format_type:
            raise click.BadParameter('must provide either --stage-name or'
                                     ' --format-type')
        stage_name = f'plow_stage_{format_type}'
    for key in s3_files:
        click.echo('Staging document %s to Snowflake...' % key, nl=False)
        op.stage_document(
            cursor=cursor,
            config=cfg,
            s3_key=key,
            stage_name=stage_name,
            tables=source.tables.keys(),
        )
        click.echo('Done!')
    click.echo('Finished all docs. Now do "transform" and "load"!')


@cli.command(name='list-tables')
@source_option_decorator
def list_tables(source):
    """List available tables."""
    for table_name in source.tables:
        click.echo(table_name)


def _etl_op(name=None):
    def wrapper(f):
        @cli.command(name=name or f.__name__)
        @source_option_decorator
        @click.argument('tables', nargs=-1)
        @wraps(f)
        @use_config
        def wrapped(cfg, source, tables):
            if not tables:
                raise click.MissingParameter(
                    'provide "ALL" or use "list-tables" for possible values',
                    param_type='argument', param_hint='TABLES')
            opname = f.__name__
            if len(tables) == 1 and tables[0] == 'ALL':
                tables = source.tables.keys()
            else:
                bad_table = next((t for t in tables if t not in source.tables),
                                 None)
                if bad_table is not None:
                    raise click.BadParameter(f'invalid table {bad_table}',
                                             param_hint='TABLES')
            for table_name in tables:
                click.echo(f'starting to {opname} table {table_name}...',
                           nl=False)
                operation = getattr(op.etl, opname)
                table = source.tables[table_name]
                operation(table=table, config=cfg)
                click.echo('Done!')
            f()
        return wrapped
    return wrapper


@_etl_op('create-tables')
def create_tables():
    """Create etl tables for the given data source"""


@_etl_op()
def transform():
    """Transform data to tabular format.

    This adds rows to a "staging" table. To perform the deduping operation and
    add data to the main table you specified, do the "load" operation after
    this.

    Requires "stage" and "create-tables" to be performed beforehand.
    """
    click.echo('Finished all tables!'
               ' Now do "load" to dedupe and complete the process')


@_etl_op()
def load():
    """Merge new data and eliminate duplicates.

    This merges rows from the "staging" table to the main table. The staging
    table must be populated by performing "transform" beforehand.
    """
    click.echo('Finished all tables! Now check snowflake for updated data')


@cli.command()
@click.option('--snowflake/--no-snowflake', default=False,
              help='initialize a snowflake connection')
@use_config
def shell(cfg, snowflake, **kwargs):
    """Play with an environment in a Python REPL."""
    import pdb
    try:
        code.interact('cfg is your current configuration.'
                      ' pdb is also available.',
                      local={'Config': Config, 'cfg': cfg, 'pdb': pdb})
    except KeyboardInterrupt:
        print('peace!')


def _config_file_cb(ctx, param, value):
    if os.path.exists(value):
        raise click.BadParameter(f'File {value} already exists!')
    return value


@cli.command(name='generate-config')
@click.option('-o', '--out', callback=_config_file_cb,
              type=click.types.Path(dir_okay=False, writable=True),
              default='mr-plow.ini')
@click.option('-b', '--blank/--no-blank', default=False,
              help='if true, ignore environment vars in constructing stub.')
@use_config
def generate_config(cfg, out, blank):
    """Generate a stub configuration file."""
    with open(out, 'w') as f:
        f.write('[mr-plow]\n')
        unseen = blank
        for k, desc in (
            ('snowflake_account',
             "subdomain from your organization's snowflake URL"),
            ('snowflake_user', "mr plow's snowflake login"),
            ('snowflake_password', None),
            ('snowflake_role', None),
            ('snowflake_database', 'database for Mr Plow to insert to'),
            ('snowflake_warehouse', 'snowflake warehouse to use for ETL'),
            (None, None),
            ('livechat_login', "your organization's livechat login"),
            ('livechat_api_key', None),
            (None, None),
            ('aws_access_key_id', 'aws access key for inserting S3 docs'),
            ('aws_secret_access_key', None),
            ('staging_aws_access_key_id',
             'aws access key to provide to Snowflake for reading S3 docs'),
            ('staging_aws_secret_access_key', None),
            (None, None),
            ('snapfulfil_login', "your organization's snapfulfil login"),
            ('snapfulfil_password', None),
            ('snapfulfil_api_domain',
             "e.g. https://treltestapi.snapfulfil.com"),
            (None, None),
            ('plow_source_module',
             "if you write your own Mr. Plow adapter, you can point to it"
             " here. Use dot notation e.g. plow.vendors.snapfulfil"),
            ('plow_source_object',
             "the above module must contain a plow.cli.Source-like object."),
        ):
            if k is not None:
                val = None if blank else getattr(cfg, k)
                if val is None:
                    unseen = True
                    val = '[UNSPECIFIED]'
                f.write(k)
                f.write(' = ')
                f.write(val)
                if desc is not None:
                    f.write('\n# ')
                    f.write(desc)
            f.write('\n\n')

        if unseen:
            f.write('\n# please replace "[UNSPECIFIED]" above with the'
                    ' appropriate value for each config parameter\n')
    click.echo(f'Wrote config to {out}!')
    if unseen:
        click.echo('It is a stub, please inspect and fill in missing values.')


def _get_default_key_format(source):
    if source.source == 'snapfulfil':
        page_param = 'skip={$skip}'
    elif source.source == 'livechat':
        page_param = 'page={page}'
    else:
        page_param = ''
    now = datetime.utcnow().isoformat()
    return f'from-cli/{source.source}/now={now}/{page_param}/data.json'


def main(obj=None):
    if obj is None:
        obj = {}
    return cli(obj=obj)


if __name__ == '__main__':
    main()
