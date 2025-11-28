from datetime import timedelta

import jwt
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction
from django.utils import timezone
from django_otp.forms import OTPAuthenticationFormMixin
from django_otp.plugins.otp_email import conf
from django_otp.plugins.otp_email.models import EmailDevice
from django_otp.util import random_hex
from two_factor.plugins.registry import registry
from two_factor.utils import default_device

from . import formfields, signals
from .app_settings import app_settings
from ..core import formfields as core_formfields, _
from ..user import formfields as user_formfields

UserModel = get_user_model()


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    phone_number/role logins.
    """
    PHONELESS_CREATION_ROLES = app_settings.PHONELESS_CREATION_ROLES

    phone_number = core_formfields.PhoneNumberField()

    role = user_formfields.RoleField()

    error_messages = {
        "invalid": _("The phone number is not associated with an account."),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, **kwargs):
        """
        The __init__ function is called every time an object is created from a class.
        The __init__ method lets the class initialize the object's attributes and serves no other purpose.
        It is only used within classes.
        """
        self.user_cache = None
        super(AuthenticationForm, self).__init__(**kwargs)

    def clean(self):
        """
        This method can perform validation that requires access to multiple form fields.

        If, at any time, any of the methods raise ValidationError,
        the validation stops and that error is raised.

        This method returns the clean data,
        which is then inserted into the cleaned_data dictionary of the form.
        """
        phone_number = self.cleaned_data.get("phone_number")
        role = self.cleaned_data.get("role")

        try:
            user = UserModel.objects.get(phone_number=phone_number, role=role)
        except (UserModel.DoesNotExist,):
            if role in self.PHONELESS_CREATION_ROLES:
                user = UserModel.objects.create_user(phone_number, role)
                signals.user_registered.send(sender=user.__class__, user=user)
            else:
                raise self.get_invalid_login_error()
        else:
            self.confirm_login_allowed(user)

        self.user_cache = user
        return self.cleaned_data

    def get_user(self):
        """
        This method returns the data of the logged-in user.
        If there is no user, the value is returned None.
        """
        return self.user_cache

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active and none deleted users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_login_allowed:
            raise ValidationError(self.error_messages["inactive"], code="inactive")

    def get_invalid_login_error(self):
        """
        This method must be called when authentication of user data fails,
        where this function return ValidationError of type invalid_login.
        """
        return ValidationError(self.error_messages["invalid"], code="invalid")

    def save(self):
        """
        Generates a challenge value that the user will need to produce a token.
        This method is permitted to have side effects, such as transmitting
        information to the user through some other channel (email or SMS,
        perhaps). And, of course, some devices may need to commit the
        challenge to the database.
        """
        return self.user_cache


class SendOTPTokenForm(AuthenticationForm):
    """
    class for send otp to users. this form requests the user's phone number,
    sending method and role of user.
    """
    method = formfields.MethodField()

    def __init__(self, request, **kwargs):
        """
        The __init__ function is called every time an object is created from a class.
        The __init__ method lets the class initialize the object's attributes and serves no other purpose.
        It is only used within classes.
        """
        self.request = request
        super(SendOTPTokenForm, self).__init__(**kwargs)

    def get_key(self):
        """
        Return A hex-encoded secret key of up to 40 bytes. (Default: 20 random bytes)
        """
        return random_hex(20)

    def get_method(self, method_key):
        """
        allowing users to authenticate through call,
        text messages (SMS) or by using a token generator app like Google Authenticator.
        """
        return registry.get_method(method_key)

    def get_device(self, request, user, **kwargs):
        """
        Returns the OTP device selected by the user, or his default device.
        """
        device = default_device(user)

        if not device:
            request.user = user
            method = self.get_method(kwargs.get('method'))
            storage_data = {method.code: {'number': user.get_phone_number()}}
            device = method.get_device_from_setup_data(self.request, storage_data, key=self.get_key())
            device.save()

        return device

    def send_otp(self, request, user, method):
        """
        Sends an OTP to the specified user, unless the user is a developer.
        @return A boolean value indicating whether the OTP was sent successfully.
        """
        if user.is_developer:
            return False

        device = self.get_device(request, user, method=method)
        return device.generate_challenge()

    def save(self):
        """
        This method can perform validation that requires access to multiple form fields.

        If, at any time, any of the methods raise ValidationError,
        the validation stops and that error is raised.

        This method returns the clean data,
        which is then inserted into the cleaned_data dictionary of the form.
        """
        self.send_otp(self.request, self.user_cache, self.cleaned_data['method'])
        return self.user_cache


class VerifyOTPTokenForm(AuthenticationForm, OTPAuthenticationFormMixin):
    """
    Class to authenticate the user by passing his token sent via SMS,call or any other method.

    If the code is correct, it can be considered that the user has been authenticated,
    and thus he can log in to the system or perform any transaction that requires user authentication.
    """
    PHONELESS_CREATION_ROLES = []

    otp_token = formfields.OTPTokenField()

    def verify_otp(self, otp, user):
        """
        Verify the given OTP with the secret key and timestamp.
        If the user is "developer", a different model is used for OTP verification.
        @return: True if the OTP is valid, False otherwise.
        """
        if user.is_developer:
            return True

        return self.clean_otp(user)

    def clean(self):
        """
        This method can perform validation that requires access to multiple form fields.

        If, at any time, any of the methods raise ValidationError,
        the validation stops and that error is raised.

        This method returns the clean data,
        which is then inserted into the cleaned_data dictionary of the form.
        """
        cleaned_data = super(VerifyOTPTokenForm, self).clean()
        otp_token = cleaned_data['otp_token']

        if settings.USE_SMS_SERVICE:
            self.verify_otp(otp_token, self.user_cache)

        return cleaned_data

    def save(self):
        """
        In the event of successful login,
        a signal is sent through the user_logging signal to the receiver
        informing him of the success of the login and recording the login time in the database.
        """
        user = self.get_user()
        signals.user_logging.send(sender=user.__class__, user=user)
        return user


class LoginForm(AuthenticationForm):
    """
    This Form is used to allow the user to log into the system by requesting the following data.
    Username (either username or email - or phone number).
    Password (stored in the database).
    """
    phone_number = None

    username = formfields.UsernameField()

    password = formfields.PasswordField()

    error_messages = {
        "invalid": _("The username or password is incorrect."),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        self.request = request
        super(LoginForm, self).__init__(**kwargs)

    def user_credentials(self):
        """
        Provides the credentials required to authenticate the user for login.
        """
        return {
            'username': self.cleaned_data['username'],
            'password': self.cleaned_data['password'],
            'role': self.cleaned_data['role']
        }

    def clean_username(self):
        """
        This method is used to clean username like strip any username
        """
        return self.cleaned_data['username'].strip()

    def clean(self):
        """
        This method can perform validation that requires access to multiple form fields.

        If, at any time, any of the methods raise ValidationError,
        the validation stops and that error is raised.

        This method returns the clean data,
        which is then inserted into the cleaned_data dictionary of the form.
        """
        credentials = self.user_credentials()
        self.user_cache = authenticate(self.request, **credentials)

        if self.user_cache:
            self.confirm_login_allowed(self.user_cache)
        else:
            raise self.get_invalid_login_error()

        return self.cleaned_data



class ResetPasswordForm(SendOTPTokenForm):
    """
    Form for handling password reset requests.
    Extend this to create a form that accepts phone number and role for user authentication.
    """
    PHONELESS_CREATION_ROLES = None

    phone_number = None

    email = core_formfields.EmailField()

    method = forms.CharField(widget=forms.HiddenInput(), initial="email")

    error_messages = {
        "invalid": _("The email is not associated with an account."),
        "inactive": _("This account is inactive."),
    }

    def clean(self):
        """
        This method can perform validation that requires access to multiple form fields.

        If, at any time, any of the methods raise ValidationError,
        the validation stops and that error is raised.

        This method returns the clean data,
        which is then inserted into the cleaned_data dictionary of the form.
        """
        email = self.cleaned_data.get("email")
        role = self.cleaned_data.get("role")

        try:
            user = UserModel.objects.get(email=email, role=role)
        except (UserModel.DoesNotExist,):
            raise self.get_invalid_login_error()
        else:
            self.confirm_login_allowed(user)

        self.user_cache = user
        return self.cleaned_data

    def get_device(self, request, user, **kwargs):
        """
        Returns the OTP device selected by the user, or his default device.
        """
        device = EmailDevice.objects.devices_for_user(self.user_cache).first()

        if not device:
            device = EmailDevice(user=self.user_cache, name='default')

        return device

    # def send_otp(self, request, user, method):
    #     """
    #     Sends an OTP to the specified user, unless the user is a developer.
    #     @return A boolean value indicating whether the OTP was sent successfully.
    #     """
    #     device = self.get_device(request, user, method=method)
    #     device.generate_token(valid_secs=conf.settings.OTP_EMAIL_TOKEN_VALIDITY)
    #     return Resend(device).send_email()


class ResetPasswordConfirmForm(ResetPasswordForm, OTPAuthenticationFormMixin):
    """
    Form for handling password reset requests.
    Extend this to create a form that accepts phone number and role for user authentication.
    """
    otp_token = formfields.OTPTokenField()

    password = user_formfields.PasswordField()

    confirm_password = user_formfields.ConfirmPasswordField()

    def __init__(self, **kwargs):
        self.error_messages.update({"mismatch": _("The passwords do not match. Please enter the same password in both fields.")})
        super().__init__(**kwargs)

    def verify_otp(self, otp, user):
        """
        Verify the given OTP with the secret key and timestamp.
        If the user is "developer", a different model is used for OTP verification.
        @return: True if the OTP is valid, False otherwise.
        """
        return self.clean_otp(user)

    def clean(self):
        """
        This method can perform validation that requires access to multiple form fields.

        If, at any time, any of the methods raise ValidationError,
        the validation stops and that error is raised.

        This method returns the clean data,
        which is then inserted into the cleaned_data dictionary of the form.
        """
        cleaned_data = super(ResetPasswordConfirmForm, self).clean()
        otp_token = cleaned_data['otp_token']
        self.verify_otp(otp_token, self.user_cache)
        return cleaned_data

    def clean_confirm_password(self):
        """
        Validate that the password and confirm_password fields match.
        """
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(self.error_messages['mismatch'])

        return confirm_password

    def save(self):
        """
        In the event of successful login,
        a signal is sent through the user_logging signal to the receiver
        informing him of the success of the login and recording the login time in the database.
        """
        self.user_cache.set_password(self.cleaned_data['password'])
        self.user_cache.save()
        return self.user_cache
