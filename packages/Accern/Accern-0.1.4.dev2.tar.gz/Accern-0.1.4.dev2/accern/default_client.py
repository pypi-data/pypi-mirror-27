from accern import error, util
import re
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
    'new_http_client'
]


def new_http_client(*args, **kwargs):
    return RequestsClient(*args, **kwargs)


class AccernClient(object):
    @staticmethod
    def check_token(token):
        if token:
            my_token = token
        else:
            from accern import token
            my_token = token

        if my_token is None:
            raise error.AuthenticationError('No token provided.')
        return my_token

    @staticmethod
    def api_encode(params):
        if isinstance(params, object):
            for key, value in util.six.iteritems(params):
                key = util.utf8(key)
                if value is None:
                    continue
                elif isinstance(value, list):
                    yield (key, ",".join(value))
                else:
                    yield (key, util.utf8(value))

    @staticmethod
    def build_api_url(url, query):
        scheme, netloc, path, base_query, fragment = util.urlsplit(url)
        if base_query:
            query = '%s&%s' % (base_query, query)
        return util.urlunsplit((scheme, netloc, path, query, fragment))

    @staticmethod
    def get_params(filters):
        param_values = [
            'entity_competitors', 'entity_country', 'entity_figi',
            'entity_indices', 'entity_industry', 'entity_market_sector',
            'entity_region', 'entity_sector', 'entity_security_type',
            'entity_ticker', 'entity_type', 'event', 'event_group', 'from',
            'last_id', 'story_type', 'story_group_exposure'
        ]
        avail_params = [value for value in filters if value in param_values]
        return {key: filters[key] for key in avail_params}

    @staticmethod
    def select_fields(options, raw_data):
        data_filtered = []

        names = [option['name'] if 'name' in option else option['field']for option in options]
        fields = [option['field'] for option in options]
        for data in raw_data:
            if bool(options) > 0:
                try:
                    if isinstance(options, list):
                        new_data = dict(zip(
                            names,
                            [data[field] for field in fields]
                        ))
                    else:
                        raise error.AccernError('Invalid select values passed.')
                except KeyError:
                    raise error.AccernError('Invalid select values passed.')
            else:
                new_data = data

            if 'entity_competitors' in new_data:
                new_data['entity_competitors'] = ' | '.join(new_data['entity_competitors'])
            if 'entity_indices' in new_data:
                new_data['entity_indices'] = ' | '.join(new_data['entity_indices'])

            data_filtered.append(new_data)

        return data_filtered


class Event(object):
    SSE_LINE_PATTERN = re.compile('(?P<name>[^:]*):?( ?(?P<value>.*))?')

    def __init__(self, data='', event='message', event_id=None, retry=None):
        self.data = data
        self.event = event
        self.event_id = event_id
        self.retry = retry

    def dump(self):
        lines = []
        if self.event_id:
            lines.append('id: %s' % self.event_id)

        # Only include an event line if it's not the default already.
        if self.event != 'message':
            lines.append('event: %s' % self.event)

        if self.retry:
            lines.append('retry: %s' % self.retry)

        lines.extend('data: %s' % d for d in self.data.split('\n'))
        return '\n'.join(lines) + '\n\n'

    @classmethod
    def parse(cls, raw):
        """Given a possibly-multiline string representing an SSE message, parse it and return a Event object."""
        msg = cls()
        for line in raw.splitlines():
            m = cls.SSE_LINE_PATTERN.match(line)
            if m is None:
                # Malformed line.  Discard but warn.
                sys.stderr.write('Invalid SSE line: "%s"' % line, SyntaxWarning)
                continue

            name = m.group('name')
            if name == '':
                # line began with a ":", so is a comment.  Ignore
                continue
            value = m.group('value')

            if name == 'data':
                # If we already have some data, then join to it with a newline.
                # Else this is it.
                if msg.data:
                    msg.data = '%s\n%s' % (msg.data, value)
                else:
                    msg.data = value
            elif name == 'event':
                msg.event = value
            elif name == 'id':
                msg.event_id = value
            elif name == 'retry':
                msg.retry = int(value)

        return msg

    def __str__(self):
        return self.data


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
                    'The underlying error was: %s' % (e))
            content = result.content
            status_code = result.status_code
        except Exception as e:
            # Would catch just requests.exceptions.RequestException, but can
            # also raise ValueError, RuntimeError, etc.
            self.handle_request_error(e)
        return content, status_code, result.headers

    @staticmethod
    def handle_request_error(e):
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
