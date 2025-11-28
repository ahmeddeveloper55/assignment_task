from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .. import serializers, permissions, jwt_response
from ...core import viewsets


class LoginViewSet(viewsets.GenericViewSet):
    """
    View for handling the login process, including OTP verification.

    The login process is composed like a wizard. The first step asks for the
    user's credentials. If the credentials are correct, the wizard proceeds to
    the OTP verification step. If the user has a default OTP device configured,
    that device is asked to generate a token (send sms / call phone) and the
    user is asked to provide the generated token.
    """
    permission_classes = (permissions.LoginAccessPolicy,)
    serializer_class = serializers.LoginSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        This API is used to login to system using username, password and role.

        If the code is correct, it can be considered that the user has been authenticated,
        and thus he can log in to the system or perform any transaction that requires user authentication.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_verify(serializer)
        response = self.get_jwt_response(instance)
        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='send-otp-token')
    def send_otp_token(self, request, *args, **kwargs):
        """
        The OTP API is an essential component of the user authentication process within this application.
        It allows users to receive OTPs via SMS messages or phone calls,
        enabling secure and reliable login functionality. By integrating this API,
        developers can enhance the security of their application and protect user accounts from unauthorized access.
        """
        serializer = serializers.SendOTPTokenSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_send_otp(serializer)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='verify-otp-token')
    def verify_otp_token(self, request, *args, **kwargs):
        """
        This API is used to verify the OTP token of the user.

        If the code is correct, it can be considered that the user has been authenticated,
        and thus he can log in to the system or perform any transaction that requires user authentication.
        """
        serializer = serializers.VerifyOTPTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_verify(serializer)
        response = self.get_jwt_response(instance)
        return Response(response, status=status.HTTP_201_CREATED)

    def get_jwt_response(self, user):
        """
        Returns the response data for both the login and refresh views.
        Override to return a custom response such as including the
        serialized representation of the User.
        @return: user payload
        """
        return jwt_response.jwt_response_payload_handler(user, request=self.request)

    def perform_send_otp(self, serializer):
        serializer.save()

    def perform_verify(self, serializer):
        instance = serializer.save()
        return instance




class PasswordViewSet(viewsets.GenericViewSet):
    """
    View for handling the password reset process, including OTP verification.

    The password reset process is composed like a wizard. The first step asks for the
    user's credentials. If the credentials are correct, the wizard proceeds to
    the OTP verification step. If the user has a default OTP device configured,
    that device is asked to generate a token (send SMS / call phone), and the
    user is asked to provide the generated token.
    """
    permission_classes = (permissions.RestPasswordAccessPolicy,)
    serializer_class = serializers.ResetPasswordSerializer
    http_method_names = ['post']

    def perform_reset(self, serializer):
        """
         Perform the action of sending OTP.
         @param serializer: The serializer instance.
         """
        serializer.save()

    def perform_verify(self, serializer):
        """
        Perform the action of verifying OTP.

        @param serializer: The serializer instance.
        @return: The saved instance after verification.
        """
        instance = serializer.save()
        return instance

    @action(detail=False, methods=['post'])
    def reset(self, request, *args, **kwargs):
        """
        This API is used to initiate the password reset process using the user's phone number, role, and email.

        If the initial validation is correct, the user proceeds to the OTP verification step,
        where they need to provide the OTP sent to their registered device.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_reset(serializer)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def change(self, request, *args, **kwargs):
        """
        Endpoint to change the user's password after verifying the OTP token.

        If the token is correct, the user is authenticated, allowing them to reset their password.
        """
        serializer = serializers.ResetPasswordConfirmSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_verify(serializer)
        return Response(status=status.HTTP_200_OK)
