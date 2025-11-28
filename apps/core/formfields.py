from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .utils.translation import _
from .app_settings import app_settings
from . import get_timezone_choices


class PhoneNumberField(PhoneNumberField):
    """
    This field represents the field for the phone number,
    as it can be used in all forms built through Django framework.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("label", _('phone number'))
        kwargs.setdefault("required", True)
        super(PhoneNumberField, self).__init__(**kwargs)


class EmailField(forms.EmailField):
    """
    This field represents the field for the email,
    as it can be used in all forms built through Django framework.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("label", _('email'))
        kwargs.setdefault("required", False)
        super(EmailField, self).__init__(**kwargs)

    def clean(self, value):
        """
        Validate the given value and return its "cleaned" value as an
        appropriate Python object. Raise ValidationError for any errors.
        """
        value = value.lower()
        return super(EmailField, self).clean(value)


class TimezoneField(forms.ChoiceField):
    """
    This field represents the field for the timezone,
    as it can be used in all forms built through Django framework.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("label", _('timezone'))
        kwargs.setdefault("default", app_settings.DEFAULT_TIMEZONE)
        kwargs.setdefault("choices", get_timezone_choices())
        super(TimezoneField, self).__init__(**kwargs)


