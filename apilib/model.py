import datetime
import decimal
import inspect
import json

from dateutil import parser as dateutil_parser

class UnknownFieldException(Exception):
    pass

class Model(object):
    def __init__(self, **kwargs):
        self._data = {}
        self._populate_fields()
        for key, value in kwargs.iteritems():
            if key not in self._field_name_to_field:
                raise UnknownFieldException('Unknown field "%s"' % key)
            setattr(self, key, value)

    def to_json(self):
        return {key: self._field_name_to_field[key].to_json(value) for key, value in self._data.iteritems()}

    def to_json_str(self):
        return json.dumps(self.to_json())

    @classmethod
    def from_json(cls, obj):
        cls._populate_fields()
        kwargs = {}
        for key, value in obj.iteritems() or []:
            field = cls._field_name_to_field.get(key)
            if field:
                kwargs[key] = field.from_json(value)
        return cls(**kwargs)

    @classmethod
    def from_json_str(cls, json_str):
        return cls.from_json(json.loads(json_str))

    @classmethod
    def _populate_fields(cls):
        if not hasattr(cls, '_field_to_attr_name'):
            cls._field_to_attr_name = {}
            cls._field_name_to_field = {}
            for attr_name, attr in cls.__dict__.iteritems():
                if attr and isinstance(attr, Field):
                    cls._field_to_attr_name[attr] = attr_name
                    cls._field_name_to_field[attr_name] = attr
                    attr._name = attr_name

class Field(object):
    def __init__(self, field_type):
        self._type = field_type
        # Will be populated when the model is instantiated
        self._name = None

    def to_json(self, value):
        return self._type.to_json(value)

    def from_json(self, value):
        return self._type.from_json(value)

    def __get__(self, instance, type=None):
        if instance:
            return instance._data.get(self._name)
        else:
            return self

    def __set__(self, instance, value):
        instance._data[self._name] = value

class ListField(Field):
    def __init__(self, field_type_or_model_class):
        if inspect.isclass(field_type_or_model_class) and issubclass(field_type_or_model_class, Model):
            field_type = ModelFieldType(field_type_or_model_class)
        else:
            field_type = field_type_or_model_class
        super(ListField, self).__init__(field_type)

    def to_json(self, value):
        if value is None:
            return None
        return [self._type.to_json(item) for item in value]

    def from_json(self, value):
        if value is None:
            return None
        return [self._type.from_json(item) for item in value]

    def __set__(self, instance, value):
        instance._data[self._name] = list(value) if value is not None else None

class ModelField(Field):
    def __init__(self, field_type_or_model_class):
        if inspect.isclass(field_type_or_model_class) and issubclass(field_type_or_model_class, Model):
            field_type = ModelFieldType(field_type_or_model_class)
        else:
            field_type = field_type_or_model_class
        super(ModelField, self).__init__(field_type)

    def to_json(self, value):
        return value.to_json() if value else None

    def from_json(self, value):
        return self._type.from_json(value) if value is not None else None

class FieldType(object):
    type_name = None
    json_type = None
    description = None

    def to_json(self, value):
        return value

    def from_json(self, value):
        return value

    # Only for documentation

    def get_type_name(self):
        return self.json_type

    def get_json_type(self):
        return self.json_type

    def get_description(self):
        return self.description

class String(FieldType):
    type_name = 'string'
    json_type = 'string'

    def to_json(self, value):
        return unicode(value) if value is not None else None

    def from_json(self, value):
        return unicode(value) if value is not None else None

class Integer(FieldType):
    type_name = 'integer'
    json_type = 'integer'

    def to_json(self, value):
        return int(value) if value is not None else None

    def from_json(self, value):
        return int(value) if value is not None else None

class Float(FieldType):
    type_name = 'float'
    json_type = 'float'

    def to_json(self, value):
        return float(value) if value is not None else None

    def from_json(self, value):
        return float(value) if value is not None else None

class Boolean(FieldType):
    type_name = 'boolean'
    json_type = 'boolean'

    def to_json(self, value):
        return bool(value) if value is not None else None

    def from_json(self, value):
        return bool(value) if value is not None else None

class ModelFieldType(FieldType):
    json_type = 'object'

    def __init__(self, model_class):
        self.model_class = model_class

    def to_json(self, value):
        return value.to_json() if value is not None else None

    def from_json(self, value):
        return self.model_class.from_json(value) if value is not None else None

    def get_type_name(self):
        return 'object(%s)' % self.model_class.__name__

class DateTime(FieldType):
    type_name = 'datetime'
    json_type = 'string'
    description = 'A datetime with time zone in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm+HH:MM)'

    def to_json(self, value):
        return unicode(value.isoformat()) if value is not None else None

    def from_json(self, value):
        return dateutil_parser.parse(unicode(value)) if value else None

class Date(FieldType):
    type_name = 'date'
    json_type = 'string'
    description = 'A date in ISO 8601 format (YYYY-MM-DD)'

    def to_json(self, value):
        return unicode(value.isoformat()) if value is not None else None

    def from_json(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date() if value else None

class Decimal(FieldType):
    type_name = 'decimal'
    json_type = 'string'
    description = 'A fixed-point decimal number'

    def to_json(self, value):
        return unicode(value) if value is not None else None

    def from_json(self, value):
        return decimal.Decimal(value) if value is not None else None
