from decimal import Decimal
import json
import re

import yaml
from yaml.composer import Composer
from yaml.constructor import SafeConstructor
from yaml.parser import Parser
from yaml.reader import Reader
from yaml.resolver import BaseResolver, Resolver as DefaultResolver
from yaml.scanner import Scanner


class Resolver(BaseResolver):
    pass


Resolver.add_implicit_resolver(  # regex copied from yaml source
    '!decimal',
    re.compile(r'''^(?:
        [-+]?(?:[0-9][0-9_]*)\.[0-9_]*(?:[eE][-+][0-9]+)?
        |\.[0-9_]+(?:[eE][-+][0-9]+)?
        |[-+]?[0-9][0-9_]*(?::[0-9]?[0-9])+\.[0-9_]*
        |[-+]?\.(?:inf|Inf|INF)
        |\.(?:nan|NaN|NAN)
    )$''', re.VERBOSE),
    list('-+0123456789.')
)

for ch, vs in DefaultResolver.yaml_implicit_resolvers.items():
    Resolver.yaml_implicit_resolvers.setdefault(ch, []).extend(
        (tag, regexp) for tag, regexp in vs
        if not tag.endswith('float')
    )


class Loader(Reader, Scanner, Parser, Composer, SafeConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        SafeConstructor.__init__(self)
        Resolver.__init__(self)


def decimal_constructor(loader, node):
    value = loader.construct_scalar(node)
    return Decimal(value)


yaml.add_constructor('!decimal', decimal_constructor, Loader)


def yaml_load(stream, **kwargs):
    return yaml.load(stream, Loader, **kwargs)


class DecimalJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        if hasattr(o, 'isoformat'):
            return o.isoformat()
        return super().default(o)


def json_dumps(obj, **kwargs):
    return json.dumps(obj, cls=DecimalJsonEncoder, **kwargs)


def json_dump(obj, f, **kwargs):
    return json.dump(obj, f, cls=DecimalJsonEncoder, **kwargs)


if __name__ == '__main__':
    from io import StringIO
    doc = StringIO('foo: 0.1000')
    expected = {'foo': Decimal('0.1')}
    print('equal with yaml.load (expect False):', yaml.load(doc) == expected)
    doc.seek(0)
    print('equal with custom load (expect True):', yaml_load(doc) == expected)
