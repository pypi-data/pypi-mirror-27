"""Tests for feed module."""

from accern import StreamClient, StreamListener, error
import json
import pytest

api_base = "http://http://feed-staging.accern.com/v4/stream"


class MyStreamListener(StreamListener):
    def on_data(self, raw_data):
        data_json = json.loads(raw_data)
        print (len(data_json))

def test_fails_without_api_key():
    """An authentication error will be raised."""
    token = None
    stream = StreamClient(MyStreamListener(), token)

    pytest.raises(error.AuthenticationError, stream.performs)
