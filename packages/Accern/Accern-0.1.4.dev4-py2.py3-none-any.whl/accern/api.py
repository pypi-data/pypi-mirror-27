"""Accern REST APIs.

Core client functionality, common across all API requests (including performing
HTTP requests).
"""

from accern import default_client, error, util
from accern.default_client import AccernClient

API_BASE = "https://feed.accern.com/v4/alphas"


class API(AccernClient):
    """Perform requests to the Accern API web services."""

    def __init__(self, token=None, client=None):
        """Intialize with params.

        :param client: default http client. Optional
        :param token: Accern API token. Required.
        """
        self.api_base = API_BASE
        self.token = token
        self._client = client or default_client.new_http_client()

    @staticmethod
    def interpret_response(rbody, rcode, rheaders, schema):
        try:
            if hasattr(rbody, 'decode'):
                rbody = rbody.decode('utf-8')
            parsed_rbody = util.json.loads(rbody)
            signals = parsed_rbody['signals']
            if parsed_rbody['total'] > 0:
                parsed_rbody['signals'] = AccernClient.select_fields(schema, signals)
            resp = parsed_rbody
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody, rcode, rheaders)
        if not 200 <= rcode < 300:
            raise error.APIError('API request failed.')
        return resp

    def request(self, schema=None):
        rbody, rcode, rheaders = self.request_raw(schema)
        resp = self.interpret_response(rbody, rcode, rheaders, schema)
        return resp

    def request_raw(self, schema):
        """Perform HTTP GET with credentials.

        :raises AuthenticationError: when the token is invalid.
        """
        params = AccernClient.get_params(schema)
        params['token'] = AccernClient.check_token(self.token)
        encoded_params = util.urlencode(list(AccernClient.api_encode(params)))
        abs_url = AccernClient.build_api_url(self.api_base, encoded_params)

        rbody, rcode, rheaders = self._client.request('GET', abs_url, headers=None, post_data=None)
        return rbody, rcode, rheaders
