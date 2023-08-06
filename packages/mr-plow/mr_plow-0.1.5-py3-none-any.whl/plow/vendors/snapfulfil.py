import collections
import io

import ijson

from .. import cli
from ..config import Config
from ..op.base import get_config
from ..op.extract import RestExtractor
from ..queries.snapfulfil import tables


def parse_json_array_for_length(data):
    with io.BytesIO(data) as data:
        parser = ijson.parse(data)
        if next(parser) != ('', 'start_array', None):
            raise ValueError('Non-array arg')
        length = 0
        for prefix, event, value in parser:
            if prefix == '' and event == 'end_array':
                break
            if prefix == 'item' and event == 'start_map':
                length += 1
    return length


SnapRequest = collections.namedtuple('SnapRequest', 'r len')
DEFAULT_PAGE_SIZE = 25


class Extractor(RestExtractor):
    def preprocess_args(self, config, kwargs):
        config = get_config(Config(config, plow_data_source='snapfulfil'),
                            'snapfulfil_api_domain', 'snapfulfil_login',
                            'snapfulfil_password')

        domain = config.snapfulfil_api_domain
        kwargs.setdefault('url', f'{domain}/api/shipments')
        kwargs['auth'] = (config.snapfulfil_login, config.snapfulfil_password)

        params = kwargs.setdefault('params', {})
        params.setdefault('$orderby', 'DateCreated asc')
        params['$top'] = int(
            params.get('$top', config.snapfulfil_page_size or 0)
        ) or DEFAULT_PAGE_SIZE

        return super().preprocess_args(config, kwargs)

    def get_data(self, *args, **kwargs):
        """Read length exactly once."""
        r = super().get_data(*args, **kwargs)
        length = parse_json_array_for_length(r.content)
        if length == 0:
            return None
        return SnapRequest(r, length)

    def postprocess_response(self, request, get_data_args):
        """Yes if we got as many results as we asked for."""
        params = get_data_args.get('params', {})
        if request.len >= params['$top']:
            new_skip = params.get('$skip', 0) + request.len
            return {**get_data_args, 'params': {**params, '$skip': new_skip}}
        # otherwise there's nothing else to do
        return None

    def encode_text(self, request):
        return super().encode_text(request.r)


source = cli.Source(source='snapfulfil', extractor=Extractor(), tables=tables)
