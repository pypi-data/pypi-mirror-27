from accern import error
import sys
import textwrap


try:
    import requests
except ImportError:
    requests = None
else:
    try:
        # Require version 0.8.8, but don't want to depend on distutils
        version = requests.__version__
        major, minor, patch = [int(i) for i in version.split('.')]
    except Exception:
        # Probably some new-fangled version, so it should support verify
        pass
    else:
        if (major, minor, patch) < (0, 8, 8):
            sys.stderr.write(
                'Warning: the Accern library requires that your Python '
                '"requests" library be newer than version 0.8.8, but your '
                '"requests" library is version %s. Accern will fall back to '
                'an alternate HTTP library so everything should work. We '
                'recommend upgrading your "requests" library. If you have any '
                'questions, please contact support@accern.com. (HINT: running '
                '"pip install -U requests" should upgrade your requests '
                'library to the latest version.)' % (version,))
            requests = None


__all__ = [
    'new_default_http_client'
]


def new_default_http_client(*args, **kwargs):
    return RequestsClient(*args, **kwargs)


class HTTPClient(object):
    def request(self, method, url, headers, post_data=None):
        raise NotImplementedError(
            'HTTPClient subclasses must implement `request`')


class RequestsClient(HTTPClient):
    name = 'requests'

    def __init__(self, timeout=80, session=None, **kwargs):
        super(RequestsClient, self).__init__(**kwargs)
        self._timeout = timeout
        self._session = session or requests.Session()

    def request(self, method, url, headers, post_data=None):
        kwargs = {}
        try:
            try:
                result = self._session.request(method,
                                               url,
                                               headers=headers,
                                               data=post_data,
                                               timeout=self._timeout,
                                               **kwargs)
            except TypeError as e:
                raise TypeError(
                    'Warning: It looks like your "requests" library is out of '
                    'date. You can fix that by running "pip install -U requests".) '
                    'The underlying error was: %s' % (e,))
            content = result.content
            status_code = result.status_code
        except Exception as e:
            # Would catch just requests.exceptions.RequestException, but can
            # also raise ValueError, RuntimeError, etc.
            self._handle_request_error(e)
        return content, status_code, result.headers

    def _handle_request_error(self, e):
        if isinstance(e, requests.exceptions.RequestException):
            msg = ("Unexpected error communicating with Accern.  "
                   "If this problem persists, let us know at "
                   "support@accern.com.")
            err = "%s: %s" % (type(e).__name__, str(e))
        else:
            msg = ("Unexpected error communicating with Accern. "
                   "It looks like there's probably a configuration "
                   "issue locally.  If this problem persists, let us "
                   "know at support@accern.com.")
            err = "A %s was raised" % (type(e).__name__,)
            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"
        msg = textwrap.fill(msg) + "\n\n(Network error: %s)" % (err,)
        raise error.APIConnectionError(msg)
