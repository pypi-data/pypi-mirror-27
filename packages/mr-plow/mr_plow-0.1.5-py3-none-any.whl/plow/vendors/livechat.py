import io

import ijson

from ..config import Config
from .. import cli
from ..op.base import get_config
from ..op.extract import RestExtractor
from ..queries.livechat import tables


class Extractor(RestExtractor):
    def preprocess_args(self, config, kwargs):
        # add LC-specific values for the passed-in dicts
        config = get_config(Config(config, plow_data_source='livechat'),
                            'livechat_login', 'livechat_api_key')
        kwargs['auth'] = (config.livechat_login, config.livechat_api_key)
        kwargs.setdefault('url', 'https://api.livechatinc.com/chats')
        kwargs.setdefault('params', {})['include_pending'] = '1'
        kwargs.setdefault('headers', {})['X-API-VERSION'] = '2'
        return super().preprocess_args(config, kwargs)

    def postprocess_response(self, request, get_data_args):
        """Validate requested page number against number of pages returned."""
        params = get_data_args.get('params', {})
        current_page = params.get('page', 1) or 1
        with io.BytesIO(request.content) as content:
            total_pages = next(ijson.items(content, 'pages'))
        if current_page < int(total_pages):
            return {**get_data_args, 'params': {**params,
                                                'page': current_page + 1}}


source = cli.Source(source='livechat', extractor=Extractor(), tables=tables)
