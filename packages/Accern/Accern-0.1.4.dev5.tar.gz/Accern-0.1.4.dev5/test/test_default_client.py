from accern import AccernClient, error
import pytest


def test_fails_with_invalid_schema():
    schema = {
        'select': [
            {
                'field': 'entity_ticker',
                'name': 'ticker'
            },
            {
                'field': 'harvested_at',
                'name': 'time'
            }
        ],
        'filters': {
            'entity': [
                "AAPL", "GOOG"
            ],
            'entity_sentiment':[
                [0, 25],
                [50, 75]
            ]
        }
    }

    with pytest.raises(error.AccernError):
        AccernClient.check_schema(schema)
