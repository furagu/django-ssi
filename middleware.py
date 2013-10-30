# -*- coding: utf-8 -*-

from funcy import *
import requests

EXTERNAL_HOST = 'http://www.redom.ru'
DEFAULT_ENCODING = 'utf-8'

"""
TODO:
 - accurate settings
 - threads to reduce processing time
 - permissive include directive support (virtual vs file, spaces everywhere)
 - timeouts
 - error handling
"""

class SsiMiddleware(object):
    def process_response(self, request, response):
        includes = set(re_all(r'<!--# include virtual=".*?" -->', response.content))
        responses = {}
        for include in includes:
            uri = re_find(r'virtual="(.*?)"', include)
            url = '%s%s' % (EXTERNAL_HOST, uri)
            r = requests.get(url)
            if 'charset' not in r.headers.get('content-type', ''):
                r.encoding = DEFAULT_ENCODING
            responses[include] = r.text.encode('utf-8')
        for include, replacement in responses.items():
            response.content = response.content.replace(include, replacement)

        return response
