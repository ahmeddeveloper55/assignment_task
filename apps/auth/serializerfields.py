from rest_framework import serializers
from two_factor.utils import totp_digits

from ..core import _, serializerfields as core_serializerfields
from . import get_methods_choices


class MethodField(serializers.ChoiceField):
    """
    This field represents the field for the method,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", _('method'))
        kwargs.setdefault("required", True)
        kwargs.setdefault("choices", get_methods_choices())
        super(MethodField, self).__init__(*args, **kwargs)


class OTPTokenField(serializers.RegexField):
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


class EmailField(core_serializerfields.EmailField):
    """
    This field represents the field for the method,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("required", True)
        super(EmailField, self).__init__(**kwargs)
