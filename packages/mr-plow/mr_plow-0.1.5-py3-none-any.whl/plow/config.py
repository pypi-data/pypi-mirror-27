"""Configuration handler.

It takes configuration from a file.

Mr. Plow is designed to run on AWS Lambda, where some configuration (notably
AWS credentials) are supplied via environment variables. As such, this
configuration handler looks to environment variables for config options that
are not given explicitly.
"""
from configparser import ConfigParser
import io
import json
import os
import re
import sys

import boto3
from snowflake.connector import connect as snowflake_connect
import yaml


_missing = object()
_doc = __doc__


class _config:
    """Config property

    Resolves from Config kwargs or environment variable.

    At most one parameter `alt` is accepted, either an alternative environment
    variable or a function to fall back on if not directly provided via kwarg
    or environment. In the latter usage it may be used as a decorator.
    """

    class doc_attr:
        def __get__(self, obj, cls=None):
            doc = object.__getattribute__((obj.__class__ if obj else cls),
                                          '_mydoc')
            if obj is None:
                return doc
            doc, _, _ = doc.partition('\n')
            if obj.alt:
                alt = obj.alt
                if hasattr(alt, '__call__') and alt.__doc__ is not None:
                    doc = f'{doc}:\n{alt.__doc__}'
                else:
                    doc = f'{doc} (alt: {alt!r})'
            return doc

    _mydoc = __doc__
    __doc__ = doc_attr()
    del doc_attr

    def __init__(self, alt=None):
        self.name = None
        self.alt = alt

    def __set_name__(self, owner, name):
        if not hasattr(owner, '_props'):
            owner._props = set()
        owner._props.add(name)
        self.name = name

    def __set__(self, obj, value):
        obj._params[self.name] = value

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        if self.name not in obj._params:
            val = None
            for alt in (self.name.upper(), self.alt):
                if alt is None:
                    continue
                if isinstance(alt, (str, bytes)):
                    altkey = alt

                    def alt(*args):
                        return obj._environ.get(altkey)

                newval = alt(obj, self.name)
                if newval:
                    val = newval
                    break
            obj._params[self.name] = val
        return obj._params[self.name]


_s3_patt = re.compile(r'^s3://([^/]+)/(.+)$')


class Config:
    """Stores config options.

    Resolves each option according to the following:
        1) user attribute setting (cfg.spam = 'eggs')
        2) kwargs (cfg = Config(spam='eggs'))
        3) environment variable
        4) alternate environment variable or access method
    The result is cached in self._params.

    :param _environ: specify an alternative for os.environ
    """

    __slots__ = ('_params', '_environ', '_src')

    def __init__(self, cfg=None, *, _environ=None, _src=None, **kwargs):
        if cfg is not None:
            if isinstance(cfg, Config):
                _src = _src or cfg.config_source
                if _environ is None:
                    _environ = cfg._environ
                cfg = cfg._params
            kwargs = {**cfg, **kwargs}

        self._src = _src
        self._environ = os.environ if _environ is None else _environ
        extra = ', '.join(k for k in kwargs if k not in self.__class__._props)
        if extra:
            raise ValueError(f'extra parameter(s) given: {extra}')
        bad_type = ', '.join(f'{k}={v!r}' for k, v in kwargs.items()
                             if not (v is None or isinstance(v, (str, bytes))))
        if bad_type:
            raise TypeError(
                f'all parameters must be strings or null: {bad_type}')
        self._params = kwargs

    snowflake_account = _config('SNOWSQL_ACCOUNT')
    snowflake_user = _config('SNOWSQL_USER')
    snowflake_password = _config('SNOWSQL_PASSWORD')
    snowflake_role = _config('SNOWSQL_ROLE')
    snowflake_database = _config('SNOWSQL_DATABASE')
    snowflake_warehouse = _config('SNOWSQL_WAREHOUSE')

    livechat_login = _config()
    livechat_api_key = _config()

    snapfulfil_login = _config()
    snapfulfil_password = _config()
    snapfulfil_page_size = _config()
    """Number of shipment records to fetch in each snapfulfil request"""
    snapfulfil_api_domain = _config()
    """API domain for snap API, e.g. https://treltestapi.snapfulfil.net"""

    def _get_aws_part(self, key):
        """If not found but aws_profile / staging_aws_profile is set, use ~/.aws/credentials"""  # noqa: E501
        if key.startswith('staging_aws_'):
            profile_key = 'staging_aws_profile'
            key = key.partition('_')[-1]
        else:
            assert key.startswith('aws_'), f'bad aws key {key!r}'
            profile_key = 'aws_profile'

        profile = getattr(self, profile_key)
        if not profile:
            return

        boto_sess = boto3.session.Session()
        if profile not in boto_sess.available_profiles:
            return

        return boto_sess._session._build_profile_map()[profile][key]

    aws_profile = _config()
    aws_access_key_id = _config(_get_aws_part)
    aws_secret_access_key = _config(_get_aws_part)
    aws_session_token = _config()

    staging_aws_profile = _config()
    staging_aws_access_key_id = _config(_get_aws_part)
    staging_aws_secret_access_key = _config(_get_aws_part)

    plow_data_source = _config()
    """name of data to use for staging purposes etc"""
    plow_s3_bucket = _config()
    """s3 bucket to store / fetch data"""
    plow_source_module = _config()
    """module where user-defined Source object can be found"""
    plow_source_object = _config()
    """name of user-defined Source object in above-mentioned module"""

    def snowflake(self):
        """Create a SnowflakeConnection based on this config"""
        params = {k.partition('_')[-1]: getattr(self, k)
                  for k in self._props if k.startswith('snowflake_')}
        return snowflake_connect(**params)

    def boto(self):
        """Create a boto3 Session based on this config"""
        kv = ((k, getattr(self, k)) for k in (
            'aws_access_key_id',
            'aws_secret_access_key',
            'aws_session_token',
            'aws_profile',
        ))
        kwargs = {k: v for k, v in kv if v is not None}
        if 'aws_profile' in kwargs:
            kwargs['profile_name'] = kwargs.pop('aws_profile')
        return boto3.session.Session(**kwargs)

    def make_s3_bucket(self, bucket=None):
        if bucket is None:
            bucket = self.plow_s3_bucket
        return self.boto().resource('s3').Bucket(bucket)

    @property
    def config_source(self):
        """Indicates where this config was loaded from"""
        return self._src

    # factory methods

    @classmethod
    def ignore_defaults(cls, *args, **kwargs):
        """Create a config where unspecified params are automatically None.

        Use this to ignore environment variables and disable alt functions.

        You can wrap other configs:

            cfg = Config.ignore_defaults(Config.parse_file(...))
        """
        cfg = cls(*args, **kwargs)
        for k in cls._props - cfg._params.keys():
            setattr(cfg, k, None)
        return cfg

    @classmethod
    def from_file(cls, fileobj, *, fmt, _src, **kwargs):
        """Parse a file object.

        :param fileobj: readable file object.
        :param fmt: string, one of "yaml", "json", "ini"
        :param kwargs: given to constructor
        """
        parser = getattr(cls, f'parse_{fmt}_file')
        params = parser(fileobj)
        if params is not None:
            params.update(kwargs)
            return cls(_src=_src, **params)

    @classmethod
    def from_filename(cls, filename, fmt=None, _src=None, **kwargs):
        """Read and parse a config file.

        :param filename: name of a file. Can be provided as an S3 url.
        :param fmt:
            see :meth:`from_file`. Drawn automatically from file extension if
            omitted.
        """
        if fmt is None:
            _, dot, fmt = os.path.basename(filename).rpartition('.')
            if not dot:
                raise ValueError(f'No extension found for {filename},'
                                 ' must provide `fmt` argument')
        s3_match = _s3_patt.match(filename)
        if s3_match:
            s3obj = boto3.resource('s3').Object(*s3_match.groups())
            fileobj = io.StringIO()
            s3obj.download_fileobj(fileobj)
            fileobj.seek(0)
        else:
            fileobj = open(filename, 'r')
        with fileobj:
            return cls.from_file(fileobj, fmt=fmt, _src=_src or filename,
                                 **kwargs)

    @classmethod
    def from_environment(cls, _default=None, **kwargs):
        """Find configuration in local environment.

        First checks for a file name in the environment variable
        MR_PLOW_CONFIG. If present and valid, uses that; otherwise,
        checks ~/.config/mr-plow.{ini,json,yaml}, ./setup.cfg and ./tox.ini,
        and chooses the first one that either is json/yaml or has a [mr-plow]
        config section.

        If none of these can be found, returns None.

        :see: :meth:`from_filename`
        """
        environ = kwargs.get('_environ', os.environ)
        filename = environ.get('MR_PLOW_CONFIG')
        if filename and (filename.startswith('s3://')
                         or os.path.exists(filename)):
            cfg = cls.from_filename(filename,
                                    _src=f'<MR_PLOW_CONFIG={filename}>',
                                    **kwargs)
        else:
            for filename, fmt in (
                *((f'{base}/mr-plow.{ext}', ext)
                  for base in ('.', '~/.config', *sys.path)
                  for ext in ('ini', 'json', 'yaml')),
                ('./setup.cfg', 'ini'),
                ('./tox.ini', 'ini'),
            ):
                if not os.path.exists(filename):
                    continue
                cfg = cls.from_filename(filename, fmt, **kwargs)
                if cfg is not None:
                    break
            else:
                cfg = None
        if cfg is not None:
            return cfg
        if _default is not None:
            return Config(_default)
        return None

    @classmethod
    def parse_ini_file(cls, fileobj):
        parser = ConfigParser()
        parser.read_file(fileobj)
        if parser.has_section('mr-plow'):
            fallback = object()
            base = {k: parser.get('mr-plow', k, fallback=fallback)
                    for k in cls._props}
            return {k: v for k, v in base.items() if v is not fallback}
        return None

    parse_cfg_file = parse_ini_file  # for setup.cfg
    parse_yaml_file = staticmethod(yaml.load)
    parse_json_file = staticmethod(json.load)

    __hash__ = None

    def __eq__(self, other):
        def strip(d):
            return {k: v for k, v in d.items() if v is not None}
        return isinstance(other, Config) and \
            strip(self._params) == strip(other._params)

    def __repr__(self):
        return f'Config({self._params!r}, _src={self.config_source!r})'
