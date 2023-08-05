from accern import API as AccernAPI
from accern import error
import pytest


def test_fails_without_token():
    API = AccernAPI()
    API.token = None
    with pytest.raises(error.AuthenticationError):
        API.request('get')
