from django.core import validators
from phonenumber_field.serializerfields import PhoneNumberField as DefaultPhoneNumberField
from rest_framework import serializers

from . import get_timezone_choices
from .app_settings import app_settings
from .utils.translation import _


class Field(serializers.Field):
    """
    This class is used to handel custom field.
    """

    @property
    def request(self):
        return self.context['request']

    @property
    def user(self):
        return self.request.user

    def is_post_action(self):
        return self.request.method == 'POST'

    def is_put_action(self):
        return self.request.method == 'PUT'

    def is_safe_method(self):
        return not bool(self.is_post_action() or self.is_put_action())


class CharField(Field, serializers.CharField):
    """
    This field represents the char field,
    as it can be used in all serializers built through Django Restfull framework.
    """


class ChoiceField(Field, serializers.ChoiceField):
    """
    This field represents the choice field,
    as it can be used in all serializers built through Django Restfull framework.
    """


class IntegerField(Field, serializers.IntegerField):
    """
    This field represents the integer field,
    as it can be used in all serializers built through Django Restfull framework.
    """


class FloatField(Field, serializers.FloatField):
    """
    This field represents the float field,
    as it can be used in all serializers built through Django Restfull framework.
    """


class BooleanField(Field, serializers.BooleanField):
    """
    This field represents the boolean field,
    as it can be used in all serializers built through Django Restfull framework.
    """


class DateTimeField(Field, serializers.DateTimeField):
    """
    This field represents the datetime field,
    as it can be used in all serializers built through Django Restfull framework.
    """


class DateField(Field, serializers.DateField):
    """
    This field represents the date field,
    as it can be used in all serializers built through Django Restfull framework.
    """


class ListField(Field, serializers.ListField):
    """
    This field represents the list field,
    as it can be used in all serializers built through Django Restfull framework.
    """


class HiddenField(Field, serializers.HiddenField):
    """
    This field represents the hidden field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def get_default(self):
        """
        Return the default value to use when validating data if no input
        is provided for this field.
        """
        return self.default


class PrimaryKeyRelatedField(Field, serializers.PrimaryKeyRelatedField):
    """
    This field represents the primary key related field,
    as it can be used in all serializers built through Django Restfull framework.
    """


class ObjectIdField(Field, serializers.UUIDField):
    """
    This field represents the object id,
    as it can be used in all serializers built through Django Restfull framework.
    """


class GenericField(Field, serializers.RelatedField):
    """
    This field represents the generic id,
    as it can be used in all serializers built through Django Restfull framework.
    """


class ParentField(HiddenField):
    """
    This field represents parent field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, default, **kwargs):
        super(ParentField, self).__init__(default=default, **kwargs)

    def validate_empty_values(self, data):
        """
        Validate empty values, and either:

        * Raise `ValidationError`, indicating invalid data.
        * Raise `SkipField`, indicating that the field should be ignored.
        * Return (True, data), indicating an empty value that should be
          returned without any further validation being applied.
        * Return (False, data), indicating a non-empty value, that should
          have validation applied as normal.
        """
        status, value = super(ParentField, self).validate_empty_values(data)

        if value is None:
            self.fail('required')

        return status, value


class PhoneNumberField(DefaultPhoneNumberField):
    """
    This field represents the phone number,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("label", _('phone number'))
        kwargs.setdefault("required", True)
        super(PhoneNumberField, self).__init__(**kwargs)


class EmailField(serializers.EmailField):
    """
    This field represents the email,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("label", _('email'))
        kwargs.setdefault("required", False)
        super(EmailField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        """
        Validate the given value and return its "cleaned" value as an
        appropriate Python object. Raise ValidationError for any errors.
        """
        data = data.lower()
        return super(EmailField, self).to_internal_value(data)


class IDField(serializers.CharField):
    """
    This field represents the id,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("label", _('ID'))
        kwargs.setdefault("required", True)
        super(IDField, self).__init__(**kwargs)


class TimezoneField(serializers.ChoiceField):
    """
    This field represents the timezone,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("label", _('timezone'))
        kwargs.setdefault("default", app_settings.DEFAULT_TIMEZONE)
        kwargs.setdefault("choices", get_timezone_choices())
        super(TimezoneField, self).__init__(**kwargs)


class SlugField(serializers.SlugRelatedField):
    """
    This field represents the slug,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("label", _('slug'))
        kwargs.setdefault("slug_field", 'slug')
        super(SlugField, self).__init__(**kwargs)








class UrlField(Field, serializers.URLField):
    """
    This field represents the url,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def to_representation(self, instance):
        return self.request.build_absolute_uri(super().to_representation(instance))


class AbsoluteUrlField(Field, serializers.SerializerMethodField):
    """
    This field represents the absolute url,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("source", 'get_absolute_url')
        kwargs.setdefault("read_only", True)
        super(AbsoluteUrlField, self).__init__(**kwargs)

    def to_representation(self, instance):
        if not hasattr(instance, 'pk'):
            return

        return self.request.build_absolute_uri(super().to_representation(instance))
