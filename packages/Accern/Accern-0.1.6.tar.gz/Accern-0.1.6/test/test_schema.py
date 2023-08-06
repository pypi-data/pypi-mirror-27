from accern import Schema, error
import pytest


def test_fails_get_options_with_invalid_field_name():
    with pytest.raises(error.SchemaError) as exc_info:
        Schema.get_options(field='test')
    assert exc_info.value.args[0] == 'Invalid field (test) in filter option.'

#########################################################
### Test Cases for func: validate_options             ###
#########################################################

def test_fails_validate_options_with_invalid_field():
    with pytest.raises(error.SchemaError) as exc_info:
        Schema.validate_options(field='test')
    assert exc_info.value.args[0] == 'Invalid field (test) in filter option.'

def test_fails_validate_options_without_value():
    with pytest.raises(error.SchemaError) as exc_info:
        Schema.validate_options(field='entity_ticker')
    assert exc_info.value.args[0] == 'No filter option value for "entity_ticker".'

def test_fails_malformed_value():
    resp = Schema.validate_options(field='entity_sentiment', value=[0, -5])
    assert resp['error'] == 'Malformed filter option value for "entity_sentiment".'

def test_fails_with_more_argument_value():
    resp = Schema.validate_options(field='entity_sentiment', value=[0, -5, 11])
    assert resp['error'] == '"entity_sentiment" has wrong number or arguments.'

def test_fails_with_less_argument_value():
    resp = Schema.validate_options(field='entity_sentiment', value=[11])
    assert resp['error'] == '"entity_sentiment" has wrong number or arguments.'

#########################################################
### Test Cases for func: validate_schema              ###
#########################################################
def test_fails_without_method():
    with pytest.raises(error.SchemaError) as exc_info:
        schema = {}
        Schema.validate_schema(schema=schema)
    assert exc_info.value.args[0] == 'Method is missing.'

def test_fails_without_schema():
    with pytest.raises(error.SchemaError) as exc_info:
        Schema.validate_schema(method='api')
    assert exc_info.value.args[0] == 'Schema is missing.'

#########################################################
### Test cases for func: validate_schema, method: api ###
#########################################################
def test_fails_with_less_argument_value_in_filters():
    with pytest.raises(error.SchemaError) as exc_info:
        schema = {
            'filters': {
                'entity_sentiment': [
                    [0, 10],
                    [15]
                ]
            }
        }
        Schema.validate_schema(method='api', schema=schema)
    assert exc_info.value.args[0] == '"entity_sentiment" has wrong number or arguments.'

#########################################################
### Test cases for func: validate_schema, method: api ###
#########################################################
def test_fails_with_less_argument_value_in_multiple_filters():
    with pytest.raises(error.SchemaError) as exc_info:
        schema = {
            'filters': [
                {
                    'entity_sentiment': [0, 10]
                },
                {
                    'entity_sentiment': [0]
                }
            ]
        }
        Schema.validate_schema(method='historical', schema=schema)
    assert exc_info.value.args[0] == '"entity_sentiment" has wrong number or arguments.'
