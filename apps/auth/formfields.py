from django import forms
from two_factor.utils import totp_digits

from . import get_methods_choices
from ..core.utils.translation import _


class MethodField(forms.ChoiceField):
    """
    This field represents the field for the method,
    as it can be used in all forms built through Django framework.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", _('method'))
        kwargs.setdefault("required", True)
        kwargs.setdefault("choices", get_methods_choices())
        super(MethodField, self).__init__(*args, **kwargs)


class OTPTokenField(forms.RegexField):
    """
    This field represents the field for the otp token,
    as it can be used in all forms built through Django framework.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", _('otp token'))
        kwargs.setdefault("required", True)
        kwargs.setdefault("regex", r'^[0-9]*$')
        kwargs.setdefault("min_length", totp_digits())
        kwargs.setdefault("max_length", totp_digits())
        super(OTPTokenField, self).__init__(*args, **kwargs)


class UsernameField(forms.CharField):
    """
    This field represents the username field,
    as it can be used in all forms built through Django framework.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", _('username'))
        kwargs.setdefault("required", True)
        super(UsernameField, self).__init__(*args, **kwargs)


class PasswordField(forms.CharField):
    """
    This field represents the password field,
    as it can be used in all forms built through Django framework.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", _('password'))
        kwargs.setdefault("required", True)
        super(PasswordField, self).__init__(*args, **kwargs)


class IDField(forms.CharField):
    """
    This field represents the id field,
    as it can be used in all forms built through Django framework.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", _('id'))
        kwargs.setdefault("required", True)
        super(IDField, self).__init__(*args, **kwargs)
