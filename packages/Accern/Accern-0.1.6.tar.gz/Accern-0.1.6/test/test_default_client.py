from accern import AccernClient, error
import pytest


def test_fails_without_token():
    with pytest.raises(error.AccernError) as exc_info:
        AccernClient.check_token(token=None)
    assert exc_info.value.args[0] == 'No token provided.'
