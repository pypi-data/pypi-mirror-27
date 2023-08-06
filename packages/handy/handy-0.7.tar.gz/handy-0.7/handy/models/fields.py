# -*- coding: utf-8 -*-
import django
from django.db import models
from django import forms
from django.core import exceptions, validators
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from handy.cross import json
from handy.forms import CommaSeparatedInput
from .encode import encode_object, decode_object, safe_encode, safe_decode

try:
    unicode
except NameError: # py3
    unicode = str
    basestring = str


__all__ = ['AdditionalAutoField', 'AdditionalAutoFieldManager',
           'BigAutoField', 'IntegerArrayField', 'BigIntegerArrayField',
           'StringArrayField', 'BigIntegerField', 'JSONField', 'PickleField']


class AdditionalAutoField(models.Field):
    """
    Additional AutoField enables you to use automatically filled but not a primary key field.
    NOTE: Doesn't work with all backends! Tested against PostgreSQL.

    Needs to be used in conjunction with AdditionalAutoFieldManager:

        class MyModel(models.Model):
            _base_manager = AdditionalAutoFieldManager()
    """
    empty_strings_allowed = False
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        models.Field.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "AutoField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                _("This value must be an integer."))

    def get_db_prep_value(self, value):
        if value is None:
            return None
        return int(value)

    def contribute_to_class(self, cls, name):
        models.Field.contribute_to_class(self, cls, name)

    def formfield(self, **kwargs):
        if self.primary_key:
            return None
        defaults = {'form_class': forms.IntegerField, 'widget': forms.HiddenInput}
        defaults.update(kwargs)
        return models.Field.formfield(self, **defaults)


class AdditionalAutoFieldManager(models.Manager):
    def _insert(self, values, **kwargs):
        # A default value should be set up by database
        values = [v for v in values
                    if v[1] is not None or not isinstance(v[0], AdditionalAutoField)]
        return super(AdditionalAutoFieldManager, self)._insert(values, **kwargs)


class BigAutoField(models.AutoField):
    def __init__(self, verbose_name=None, name=None, external_sequence=False, **kwargs):
        self.external_sequence = external_sequence
        models.AutoField.__init__(self, verbose_name, name, **kwargs)

    def db_type(self, connection):
        return 'bigint' if self.external_sequence else 'bigserial'

    # Use ForeignKey patch
    def rel_db_type(self, connection):
        return 'bigint'


class UntypedMultipleField(forms.Field):
    def __init__(self, *args, **kwargs):
        self.coerce = kwargs.pop('coerce', lambda val: val)
        super(UntypedMultipleField, self).__init__(*args, **kwargs)


class TypedMultipleField(UntypedMultipleField):
    def to_python(self, value):
        value = super(TypedMultipleField, self).to_python(value)
        if value not in validators.EMPTY_VALUES:
            try:
                value = [self.coerce(v) for v in value]
            except (ValueError, TypeError):
                raise exceptions.ValidationError(self.error_messages['invalid'])
        return value

class TypedMultipleChoiceField(TypedMultipleField, forms.MultipleChoiceField):
    def validate(self, value):
        pass


class ArrayField(models.Field):
    def value_to_string(self, obj):
        return self.get_prep_value(self.value_from_object(obj))

    def validate(self, value, model_instance):
        # This is mostly copied from Field.validate().
        # Unforturnately Field.validate() doesn't handle choices right for multivalue fields.
        if not self.editable:
            return

        if value is None and not self.null:
            raise exceptions.ValidationError(self.error_messages['null'])

        if not self.blank and value in validators.EMPTY_VALUES:
            raise exceptions.ValidationError(self.error_messages['blank'])

        # TODO: validate choices

    def formfield(self, **kwargs):
        if self.choices:
            # Also copy-pasted from Field.formfield
            defaults = {
                'choices': self.choices,
                'coerce': self.coerce,
                'required': not self.blank,
                'label': capfirst(self.verbose_name),
                'help_text': self.help_text,
                'widget': forms.CheckboxSelectMultiple
            }
            defaults.update(kwargs)
            return TypedMultipleChoiceField(**defaults)
        else:
            defaults = {
                'form_class': TypedMultipleField,
                'coerce': self.coerce,
                'widget': CommaSeparatedInput,
            }
            defaults.update(kwargs)
            return super(ArrayField, self).formfield(**defaults)


class IntegerArrayField(ArrayField):
    default_error_messages = {
        'invalid': _(u'Enter only digits separated by commas.')
    }
    description = _("Array of integers")
    coerce = int

    def db_type(self, connection):
        return 'int[]'

    def to_python(self, value):
        if value == '{}':
            return []

        if isinstance(value, basestring):
            return [self.coerce(v) for v in value[1:-1].split(',')]

        return value

    def get_prep_value(self, value):
        return '{%s}' % ','.join(map(str, value))


class BigIntegerArrayField(IntegerArrayField):
    def db_type(self, connection):
        return 'bigint[]'

# Fix unicode arrays for postgresql_psycopg2 backend
try:
    import psycopg2
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
except ImportError:
    pass

class StringArrayField(ArrayField):
    description = _("Array of strings")
    coerce = unicode

    def __init__(self, verbose_name=None, **kwargs):
        kwargs.setdefault('max_length', 127)
        super(StringArrayField, self).__init__(verbose_name, **kwargs)

    def db_type(self, connection):
        return 'varchar(%s)[]' % self.max_length


class JSONField(models.TextField):
    """JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly"""
    if django.VERSION < (1, 8):
        __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.pickle = kwargs.pop('pickle', False)
        super(JSONField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        if self.pickle:
            kwargs['pickle'] = True
        return name, path, args, kwargs

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if value in ("", None):
            return None

        try:
            if isinstance(value, (str, unicode)):
                return json.loads(value, object_hook=decode_object if self.pickle else None)
        except ValueError:
            pass

        return value

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_prep_value(self, value):
        """Convert our JSON object to a string before we save"""
        if value == "" or value is None:
            return None
        return json.dumps(value, default=encode_object if self.pickle else None,
                         ensure_ascii=False, separators=(',',':'))

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return json.dumps(value, default=encode_object if self.pickle else None,
                          ensure_ascii=False)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.CharField,
        }
        defaults.update(kwargs)
        defaults['widget'] = JSONTextarea
        return super(JSONField, self).formfield(**defaults)


class JSONTextarea(forms.Textarea):
    def value_from_datadict(self, data, files, name):
        value = data.get(name, '').strip()
        if value in ['', None]:
            return {}
        return json.loads(value)

    def render(self, name, value, attrs=None):
        return super(JSONTextarea, self).render(name, json.dumps(value), attrs=attrs)


class PickleField(models.TextField):
    """
    PickleField is a generic textfield that neatly serializes/unserializes
    any python objects seamlessly"""
    if django.VERSION < (1, 8):
        __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
        if value in ("", None):
            return None

        try:
            if isinstance(value, basestring):
                return safe_decode(value)
        except ValueError:
            pass

        return value

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_prep_value(self, value):
        """Convert our JSON object to a string before we save"""
        if value == "" or value is None:
            return None
        return safe_encode(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return safe_encode(value)


class BigIntegerField(models.IntegerField):
    def db_type(self):
        # Only for MySQL and PostgreSQL
        return "bigint"

    def get_internal_type(self):
        return "BigIntegerField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return long(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                _("This value must be a long integer."))


try:
    from south.modelsinspector import add_introspection_rules
    rules = [
        ((BigAutoField, ), [], {"external_sequence": ["external_sequence", {"default": False}]}),
        ((StringArrayField, ), [], {"max_length": ["max_length", {}]}),
    ]
    add_introspection_rules(rules, ["^handy\.models\.fields\."])
except ImportError:
    pass
