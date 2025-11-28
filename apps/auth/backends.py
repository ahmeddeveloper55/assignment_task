from django.contrib.auth import get_user_model
from phonenumber_field import phonenumber


USER_MODEL = get_user_model()


class UsernameOrPhoneNumberOrEmailBackend(object):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:

            if '@' in username:
                kwargs.update({'email': username.lower()})

            elif phonenumber.to_python(username).is_valid():
                kwargs.update({'phone_number': username})

            else:
                kwargs.update({'username': username})

            user = USER_MODEL.verified_objects.get(**kwargs)

        except (USER_MODEL.DoesNotExist, Exception):
            return None

        else:
            if user.check_password(password) and user.is_login_allowed:
                return user

    def get_user(self, user_id):
        try:
            return USER_MODEL.objects.get(pk=user_id)
        except USER_MODEL.DoesNotExist:
            return None
