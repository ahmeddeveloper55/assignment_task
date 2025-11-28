from . import mixins


class SendOTPTokenSerializer(mixins.SendOTPTokenSerializerMixin):
    """
    class for send otp to users. this form requests the user's phone number,
    sending method and role of user.
    """


class VerifyOTPTokenSerializer(mixins.VerifyOTPTokenSerializerMixin):
    """
    Class to authenticate the user by passing his token sent via SMS,call or any other method.

    If the code is correct, it can be considered that the user has been authenticated,
    and thus he can log in to the system or perform any transaction that requires user authentication.
    """


class LoginSerializer(mixins.LoginSerializerMixin):
    """
    This class is used to verify the username with the password. and it's used to
    log in user to the system.
    """






class ResetPasswordSerializer(mixins.ResetPasswordSerializerMixin):
    """
    This class provides functionality to reset a user's password by verifying
    the provided credentials and processing the password change request.
    """


class ResetPasswordConfirmSerializer(mixins.ResetPasswordConfirmSerializerMixin):
    """
    This class provides functionality to reset a user's password by verifying
    the provided credentials and processing the password change request.
    """