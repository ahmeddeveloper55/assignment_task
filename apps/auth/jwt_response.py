from datetime import datetime

from rest_framework_simplejwt.tokens import RefreshToken
from ..editor import serializers as editor_serializers


def jwt_response_payload_handler(user, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    refresh = RefreshToken.for_user(user)
    expiration_timestamp = refresh.payload["exp"]
    expiration_datetime = datetime.fromtimestamp(expiration_timestamp)
    context = {'request': request}

    response = {
        'access_token': str(refresh.access_token),
        'refresh': str(refresh),
        'expiry_date': expiration_datetime,
        'name': user.name,
        'username': user.username,
        'email': user.email,
        'phone_number': user.get_phone_number(),
        'role': user.role,
        'role_display': user.get_role_display(),
        'is_active': user.is_active,
    }

    if user.is_editor:
        editor = user.owneruser.owner
        data = editor_serializers.EditorSerializer(editor, context=context).data
        response.update({
            'name': data['name'],
            'email': data['email'],
            'image': data['image'],
        })

    return response
