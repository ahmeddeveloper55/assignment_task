from rest_framework import serializers

from . import forms, serializerfields
from ..core import serializers as core_serializers, serializerfields as core_serializerfields
from ..user import serializerfields as user_serializerfields


class SendOTPTokenSerializerMixin(core_serializers.FormSerializer):
    """
    class for send otp to users. this form requests the user's phone number,
    sending method and role of user.
    """
    phone_number = core_serializerfields.PhoneNumberField()

    role = user_serializerfields.RoleField()

    method = serializerfields.MethodField()

    form_class = forms.SendOTPTokenForm

    def get_form_class(self, attrs):
        """
        This function is used to initialize the form data
        """
        request = self.context['request']
        return self.form_class(request=request, data=attrs)


class VerifyOTPTokenSerializerMixin(core_serializers.FormSerializer):
    """
    Class to authenticate the user by passing his token sent via SMS,call or any other method.

    If the code is correct, it can be considered that the user has been authenticated,
    and thus he can log in to the system or perform any transaction that requires user authentication.
    """

    phone_number = core_serializerfields.PhoneNumberField()

    role = user_serializerfields.RoleField()

    otp_token = serializerfields.OTPTokenField()

    form_class = forms.VerifyOTPTokenForm


class LoginSerializerMixin(SendOTPTokenSerializerMixin):
    """
    This class is used to verify the username with the password. and it's used to
    log in user to the system.
    """
    phone_number = None

    method = None

    username = user_serializerfields.UsernameField()

    password = user_serializerfields.PasswordField()

    role = user_serializerfields.RoleField()

    form_class = forms.LoginForm



class ResetPasswordSerializerMixin(SendOTPTokenSerializerMixin):
    """
    This class provides functionality to reset a user's password by verifying
    the provided credentials and processing the password change request.
    """
    phone_number = None

    method = serializers.HiddenField(default='email')

    email = serializerfields.EmailField()

    role = user_serializerfields.RoleField()

    form_class = forms.ResetPasswordForm


class ResetPasswordConfirmSerializerMixin(ResetPasswordSerializerMixin, VerifyOTPTokenSerializerMixin):
    """
    Class to authenticate the user by passing his token sent via SMS,call or any other method.

    If the code is correct, it can be considered that the user has been authenticated,
    and thus he can log in to the system or perform any transaction that requires user authentication.
    """
    phone_number = None

    email = serializerfields.EmailField()

    password = user_serializerfields.PasswordField()

    confirm_password = user_serializerfields.ConfirmPasswordField()

    form_class = forms.ResetPasswordConfirmForm

