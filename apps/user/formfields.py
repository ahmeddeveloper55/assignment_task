from django import forms
from ..core.utils.translation import _
from . import validators, RoleChoices


class RoleField(forms.ChoiceField):
    """
    This field represents the field for the role,
    as it can be used in all forms built through Django framework.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", _('role'))
        kwargs.setdefault("required", True)
        kwargs.setdefault("choices", RoleChoices.choices)
        super(RoleField, self).__init__(*args, **kwargs)


class PasswordField(forms.CharField):
    """
    This field represents the password field,
    as it can be used in all forms built through Django framework.
    """
    default_validators = [validators.validate_password]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", _('password'))
        kwargs.setdefault("required", True)
        super(PasswordField, self).__init__(*args, **kwargs)


class ConfirmPasswordField(PasswordField):
    """
    This field represents the confirmation password field,
    as it can be used in all forms built through Django framework.
    """
