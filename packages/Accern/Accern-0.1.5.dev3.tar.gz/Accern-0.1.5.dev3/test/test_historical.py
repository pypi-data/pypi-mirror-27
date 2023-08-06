from accern import HistoricalClient, error
import pytest


def test_fails_without_token():
    token = None
    Client = HistoricalClient(token)
    with pytest.raises(error.AuthenticationError):
        Client.get_jobs()
