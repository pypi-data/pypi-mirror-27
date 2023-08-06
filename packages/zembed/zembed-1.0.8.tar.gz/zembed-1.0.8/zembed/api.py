import requests
import json
from simplejson import JSONDecodeError
from zembed.exceptions import ZembedException


class API:
    _api_key = None
    _base_url = 'http://api.zembed.com'

    def __init__(self, api_key):
        self._api_key = api_key

    def get_embed(self, url, **kwargs):
        if type(url) == str:
            return self._get('{}/{}'.format(self._base_url, 'embed'), {
                'url': url, 'format': 'json', **kwargs
            })
        else:
            return self._post('{}/{}'.format(self._base_url, 'embeds'), {
                'urls': json.dumps(url), 'format': 'json', **kwargs
            })

    def _get(self, url, params=None, **kwargs):
        result = requests.get(url, params=params, headers={'Authorization': self._api_key}, **kwargs)

        try:
            _response = result.json()

            if _response and 'error' in _response or result.status_code != 200:
                message = _response['error'] if 'error' in _response else _response['message']
                raise ZembedException(_response['status_code'], message, _response)

            return _response
        except JSONDecodeError:
            raise ZembedException(result.status_code, result.content.decode(), {})

    def _post(self, url, params=None, **kwargs):
        result = requests.post(url, data=params, headers={'Authorization': self._api_key}, **kwargs)

        try:
            _response = result.json()

            if _response and 'error' in _response or result.status_code != 200:
                message = _response['error'] if 'error' in _response else _response['message']
                raise ZembedException(_response['status_code'], message, _response)

            return _response
        except JSONDecodeError:
            raise ZembedException(result.status_code, result.content.decode(), {})

    @staticmethod
    def response(response):
        return response.json()
