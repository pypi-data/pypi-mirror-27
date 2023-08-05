"""Accern REST APIs.

Core client functionality, common across all API requests (including performing
HTTP requests).
"""

try:
    import requests
except ImportError:
    requests = None

from accern import error, http_client, util
from accern.util import six, urlsplit, urlunsplit, urlencode

api_base = "https://feed.accern.com/v4/alphas"


class API(object):
    """Perform requests to the Accern API web services."""

    def __init__(self, client=None, token=None):
        """Intialize with params.

        :param client: default http client. Optional
        :param token: Accern API token. Required.
        """
        self.api_base = api_base
        self.token = token
        self._client = client or http_client.new_default_http_client()

    def _api_encode(self, data):
        for key, value in six.iteritems(data):
            key = util.utf8(key)
            if value is None:
                continue
            elif isinstance(value, list):
                yield (key, ",".join(value))
            else:
                yield (key, util.utf8(value))

    def _build_api_url(self, url, query):
        scheme, netloc, path, base_query, fragment = urlsplit(url)
        if base_query:
            query = '%s&%s' % (base_query, query)
        return urlunsplit((scheme, netloc, path, query, fragment))

    def interpret_response(self, rbody, rcode, rheaders):
        try:
            if hasattr(rbody, 'decode'):
                rbody = rbody.decode('utf-8')
            resp = util.json.loads(rbody)
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody, rcode, rheaders)
        if not (200 <= rcode < 300):
            raise error.APIError('API request failed.')
        return resp

    def request(self, method, params=None):
        rbody, rcode, rheaders = self.request_raw(
            method.lower(), params)
        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp

    def request_raw(self, method=None, params=None):
        """Perform HTTP GET with credentials.

        :param method: HTTP method
        :param params: HTTP GET parameters.
        :raises AuthenticationError: when the token is invalid.
        """
        if self.token:
            my_token = self.token
        else:
            from accern import token
            my_token = token

        if my_token is None:
            raise error.AuthenticationError('No token provided.')

        abs_url = self.api_base
        if params is None:
            params = {'token': my_token}
        else:
            params['token'] = my_token
        encoded_params = urlencode(list(self._api_encode(params or {})))

        if method == 'get':
            if params:
                abs_url = self._build_api_url(abs_url, encoded_params)
        else:
            raise error.APIConnectionError('Unsupported HTTP method %r' % (method))

        rbody, rcode, rheaders = self._client.request(method, abs_url, headers=None, post_data=None)
        return rbody, rcode, rheaders
