from accern import API, error
import pytest


def test_fails_without_token():
    token = None
    Client = API(token)
    with pytest.raises(error.AuthenticationError):
        Client.request({})
