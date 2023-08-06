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
        field = kwargs.get('field')
        value = kwargs.get('value')
        if len(value) != 2:
            return {
                'field': field,
                'type': 'no range',
                'error': '"%s" has wrong number or arguments.' % (field)
            }
        if value[1] < value[0]:
            return {
                'field': field,
                'type': 'range',
                'error': 'Malformed filter option value for "%s".' % (field)
            }
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
    def get_url_params(cls):
        return [k for k, v in FIELD_OPTIONS.items() if 'url_param' in v['method']]
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
            'range': cls._validate_range,
            'other': lambda x: x
        }
        return types[FIELD_OPTIONS[field]['type']]({
            'field': field,
            'value': value
        })

    @classmethod
    def validate_schema_filters(cls, **kwargs):
        method = kwargs.get('method', None)
        filters = kwargs.get('filters', None)
        if isinstance(filters, list):
            if method != 'historical':
                raise error.SchemaError('Method "%s" does not support multiple filters.' % method)
            for f in filters:
                cls.validate_schema_filters(method=method, filters=f)
            return
        for f in filters:
            if isinstance(filters[f], list) and any(isinstance(el, list) for el in filters[f]):
                for el in filters[f]:
                    resp = cls.validate_options(field=f, value=el)
                    if 'error' in resp:
                        raise error.SchemaError(resp['error'])
            else:
                resp = cls.validate_options(field=f, value=filters[f])
                if 'error' in resp:
                    raise error.SchemaError(resp['error'])

    @classmethod
    def validate_schema_select(cls, **kwargs):
        method = kwargs.get('method', None)
        select = kwargs.get('select', None)
        if method in ['api', 'stream']:
            if any('function' in el for el in select):
                raise error.SchemaError('Method "%s" does not support select field functions.' % method)
            if isinstance(select, list):
                try:
                    return [{'field': v['field'], 'alias': v.get('alias', v['field'])} for v in select]
                except KeyError:
                    raise error.SchemaError('Missing "field" in select option.')
            else:
                try:
                    return {'field': select['field'], 'alias': select.get('alias', select['field'])}
                except KeyError:
                    raise error.SchemaError('Missing "field" in select option.')
        else:
            try:
                if any(v["field"] == 'harvested_at' and v.get("function") is not None for v in select):
                    select = [
                        {
                            'field': v['field'],
                            'alias': v.get('alias', v['field']),
                            'function': v.get('function', FIELD_OPTIONS[v['field']]['function'][0])
                        } for v in select
                    ]
                    if any(v['field'] == 'harvested_at' and v['alias'] != v['function'] for v in select):
                        raise error.SchemaError("Alias of harvested_at is different from it's aggregation function.")
                else:
                    select = [
                        {
                            'field': v['field'],
                            'alias': v.get('alias', v['field'])
                        } for v in select]
                return select
            except KeyError:
                raise error.SchemaError('Missing "field" in select option.')

    @classmethod
    def validate_schema(cls, **kwargs):
        schema = kwargs.get('schema', None)
        if schema is None:
            raise error.SchemaError('Schema is missing.')
        schema = {k.lower(): v for k, v in schema.items()}

        method = kwargs.get('method', None)
        if method is None:
            raise error.SchemaError('Method is missing.')

        if method in ['api', 'stream']:
            if 'name' in schema:
                raise error.SchemaError('Illegal "name" in %s schema.' % method)
            if 'description' in schema:
                raise error.SchemaError('Illegal "description" in %s schema.' % method)
        else:
            if 'name' not in schema:
                raise error.SchemaError('Required field "name" not found in %s schema.' % method)
            if 'description' not in schema:
                raise error.SchemaError('Required field "description" not found in %s schema.' % method)

        filters = schema.get('filters', {})
        if method in ['api', 'historical', 'stream']:
            cls.validate_schema_filters(method=method, filters=filters)
        else:
            raise error.SchemaError('Illegal usage of validate schema function.')

        select = schema.get('select', {})
        if method in ['api', 'historical', 'stream']:
            select = cls.validate_schema_select(method=method, select=select)
        else:
            raise error.SchemaError('Illegal usage of validate schema function.')
        schema['select'] = select

        return schema
