from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

USER_MODEL = get_user_model()

UserSearchFields = ['name', 'phone_number', 'email']


class UserFilter(filters.FilterSet):
    """
    This class used to filter all users based some fields and return to viewset model.
    """

    class Meta:
        model = USER_MODEL
        fields = {
            'username': ['contains'],
            'name': ['contains'],
            'role': ['exact'],
            'is_active': ['exact'],
            'phone_number': ['contains'],
            'email': ['contains'],
            'last_login': ['date__range'],
            'created_at': ['date__range'],
            'updated_at': ['date__range'],
        }
