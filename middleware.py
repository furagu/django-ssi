from funcy import *
import requests

from django.conf import settings

"""
TODO:
 - threads to reduce processing time
 - permissive include directive syntax support (virtual vs file, spaces everywhere)
 - timeouts
 - error handling
"""

class SsiMiddleware(object):
    """
    Response-phase middleware that processes SSI include directives in the text/html responses content.

    Define SSI_BASE_URL = 'http://www.your.main.host.accessible.from.this.machine' in your settings.py.
    """
    def __init__(self):
        self.base_url = settings.SSI_BASE_URL
        self.default_encoding = getattr(settings, 'SSI_DEFAULT_ENCODING', 'utf-8')

    def process_response(self, request, response):
        if response['Content-Type'].startswith('text/html'):
            includes = set(re_all(r'<!--# include virtual=".*?" -->', response.content))
            responses = {}
            for include in includes:
                include_url = re_find(r'virtual="(.*?)"', include)
                url = '%s%s' % (self.base_url, include_url)
                r = requests.get(url)
                if 'charset' not in r.headers.get('content-type', ''):
                    r.encoding = self.default_encoding
                responses[include] = r.text.encode('utf-8')
            for include, replacement in responses.items():
                response.content = response.content.replace(include, replacement)

        return response
