from accern import error
from os.path import dirname
import json

MODULE_PATH = dirname(__file__)
FIELD_OPTIONS = json.load(open("%s/data/options.json" % MODULE_PATH))

class Schema(object):
    @staticmethod
    def _validate_categorical(kwargs):
        field = kwargs.get('field')
        value = kwargs.get('value')
        VALUE = FIELD_OPTIONS[field]['value']
        return {
            'field': field,
            'type': 'categorical',
            'value': {
                'valid': [v for v in value if v in VALUE],
                'invalid': [v for v in value if v not in VALUE]
            }
        }

    @staticmethod
    def _validate_range(kwargs):
        field = kwargs.get('field')
        value = kwargs.get('value')
        RANGE = FIELD_OPTIONS[field]['value']
        if not isinstance(value, list):
            return {
                'field': field,
                'error': 'Invalid value type of field.'
            }
        if len(value) != 2:
            return {
                'field': field,
                'type': 'range',
                'error': '"%s" has wrong number or arguments.' % (field)
            }
        if value[1] < value[0]:
            return {
                'field': field,
                'type': 'range',
                'error': 'Malformed filter option value for "%s".' % (field)
            }
        if value[0] >= RANGE[0] and value[1] <= RANGE[1]:
            return {
                'field': field,
                'type': 'range',
                'value': {
                    'valid': True,
                    'default_range': RANGE
                }
            }
        return {
            'field': field,
            'type': 'range',
            'value': {
                'valid': False,
                'default_range': RANGE
            }
        }

    @staticmethod
    def _validate_norange(kwargs):
        return {
            'field': kwargs.get('field'),
            'type': 'no range'
        }

    @classmethod
    def get_fields(cls):
        return FIELD_OPTIONS.keys()

    @classmethod
    def get_options(cls, field):
        if field in FIELD_OPTIONS:
            return FIELD_OPTIONS[field]
        raise error.SchemaError('Invalid field (%s) in filter option.' % field)

    @classmethod
    def validate_options(cls, **kwargs):
        field = kwargs.get('field', None)
        value = kwargs.get('value', None)
        if field not in FIELD_OPTIONS:
            raise error.SchemaError('Invalid field (%s) in filter option.' % field)
        if value is None:
            raise error.SchemaError('No filter option value for "%s".' % field)

        types = {
            'categorical': cls._validate_categorical,
            'norange': cls._validate_norange,
            'range': cls._validate_range
        }
        return types[FIELD_OPTIONS[field]['type']]({
            'field': field,
            'value': value
        })

    @classmethod
    def validate_schema_filters(cls, method, filters):
        if isinstance(filters, list):
            for f in filters:
                cls.validate_schema_filters(method, f)
            return
        for f in filters:
            if any(isinstance(el, list) for el in filters[f]):
                for el in filters[f]:
                    resp = cls.validate_options(field=f, value=el)
                    if 'error' in resp:
                        raise error.SchemaError(resp['error'])
            else:
                resp = cls.validate_options(field=f, value=filters[f])
                if 'error' in resp:
                    raise error.SchemaError(resp['error'])

    @classmethod
    def validate_schema(cls, **kwargs):
        schema = kwargs.get('schema', None)
        if schema is None:
            raise error.SchemaError('Schema is missing.')
        method = kwargs.get('method', None)
        if method is None:
            raise error.SchemaError('Method is missing.')

        filters = schema.get('filters', {})
        if method in ['api', 'historical', 'stream']:
            cls.validate_schema_filters(method=method, filters=filters)
        else:
            raise error.SchemaError('Illegal usage of validate schema function.')
        return True
