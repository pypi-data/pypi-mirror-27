"""Resources used or potentially used in multiple test files.

pytest docs seem to discourage importing in the test package, so we follow
convention from other libraries and define these in a dedicated <pkg>.testing
module.
"""
import copy
from importlib import import_module
import operator
from os import path
import pickle
import re

from ..queries import etl_tracking
from . import decimal_encoding


STAGE = 'plow_testing_stage'
FORMAT_NAME = etl_tracking._get_file_format_name('JSON')


def make_pk(pk):
    if not isinstance(pk, (tuple, list)):
        pk = (pk,)
    return tuple(pk)


def pk_getter(pk):
    return operator.itemgetter(*make_pk(pk))


_missing = object()
in_memory_cache = {}


def get_sample_data(cache, source):
    if source in in_memory_cache:
        return in_memory_cache[source]
    dirname = cache.makedir('mr-plow-test-data')
    data = fetch_sample_data(dirname, source)
    if data is _missing:
        data = parse_sample_data(source)
        store_sample_data(dirname, source, data)
    return data


def fetch_sample_data(dirname, source):
    filename = path.join(dirname, source)
    if path.isfile(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return _missing


def store_sample_data(dirname, source, data):
    in_memory_cache[source] = data
    with open(path.join(dirname, source), 'wb') as f:
        pickle.dump(data, f)


def parse_sample_data(source):
    root = path.dirname(path.dirname(path.dirname(__file__)))
    fname = path.join(root, 'test', 'data', source + '.yaml')
    with open(fname) as f:
        return decimal_encoding.yaml_load(f)


class SampleData(object):
    def __init__(self, name, inp, out, extr):
        self.name = name
        self.input = inp
        self.output = out
        self.extract = extr

    @classmethod
    def from_dict(cls, name, val):
        return cls(name, val['input'], val['output'], val.get('extract') or {})

    def deepcopy(self):
        return SampleData(
            self.name,
            copy.deepcopy(self.input),
            copy.deepcopy(self.output),
            copy.deepcopy(self.extract),
        )

    @property
    def npages(self):
        npages = len(self.input)
        if (self.extract or {}).get('ignore_last'):
            npages -= 1
        return npages

    def json_input(self, start=None, end=None):
        """Convert input items to json.

        yields binary objects.
        """
        for inp in self.input[start:end]:
            yield decimal_encoding.json_dumps(inp).encode('ascii')


type_pattern = re.compile(r'^(\w+)')
int_number_pattern = re.compile(r'^NUMBER\((\d+),\s*0\)')


def get_sql_type(d, _make_int=False):
    if isinstance(d, dict):
        d = d['type']
    if _make_int:
        m = int_number_pattern.match(d)
        if m and int(m.group(1)) >= 38:
            d = 'INTEGER'
    t = type_pattern.match(d)
    assert t, 'match for %r' % (d,)
    return t.group(1)


available_sources = ['livechat', 'snapfulfil']


def get_source(name):
    return import_module('plow.vendors.' + name).source
