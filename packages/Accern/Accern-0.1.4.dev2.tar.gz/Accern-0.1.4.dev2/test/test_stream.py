"""Tests for feed module."""

from accern import StreamClient, StreamListener, error
# from mock import Mock
import json
import pytest

api_base = "http://http://feed-staging.accern.com/v4/stream"


class MyStreamListener(StreamListener):
    def on_data(self, data):
        data_json = json.loads(data)
        print (len(data_json))


# @pytest.fixture(scope="module")
# def client():
#     return myStreamListener()()


def test_fails_without_api_key():
    """An authentication error will be raised."""
    token = None
    myStreamListener = MyStreamListener()
    kwargs = {}
    stream = StreamClient(listener=myStreamListener, token=token, **kwargs)

    pytest.raises(error.AuthenticationError, stream.performs)


def test_fails_with_wrong_fields():
    """An authentication error will be raised."""
    token = None
    myStreamListener = MyStreamListener()
    kwargs = {
        'fields': ['entity']
    }
    stream = StreamClient(listener=myStreamListener, token=token, **kwargs)

    pytest.raises(error.AuthenticationError, stream.performs)
