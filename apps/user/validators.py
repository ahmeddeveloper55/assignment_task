import re
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from ..core import _


@deconstructible
class ASCIIUsernameValidator(ASCIIUsernameValidator):
    regex = r'^(?=.*[A-Za-z])[\w\d#$]{5,30}$'


@deconstructible
class PasswordValidator:
    """
    Validator to check if the password is at least 8 characters long,
    contains at least one letter and one digit.
    """
    requires_context = True
    message_length = _("Password must be at least 8 characters long.")
    message_letter = _("Password must contain at least one letter.")
    message_digit = _("Password must contain at least one digit.")

    def __init__(self, message_length=None, message_letter=None, message_digit=None):
        self.message_length = message_length or self.message_length
        self.message_letter = message_letter or self.message_letter
        self.message_digit = message_digit or self.message_digit

    def __call__(self, value, serializer_field=None):
        if len(value) < 8:
            raise ValidationError(self.message_length)

        if not re.search(r'[A-Za-z]', value):
            raise ValidationError(self.message_letter)

        if not re.search(r'\d', value):
            raise ValidationError(self.message_digit)


validate_username = ASCIIUsernameValidator()

# Instantiate the PasswordValidator
validate_password = PasswordValidator()