from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

USER_MODEL = get_user_model()

EditorSearchFields = ['name', 'email', 'phone_number', 'editor__name_en', 'editor__name_ar']


class EditorFilter(filters.FilterSet):
    """
    This class used to filter all users based some fields and return to viewset model.
    """
    class Meta:
        model = USER_MODEL
        fields = {
            'id': ['exact'],
            'name': ['contains'],
            'username': ['contains'],
            'phone_number': ['contains'],
            'email': ['contains'],
            'editor__name_en': ['contains'],
            'editor__name_ar': ['contains'],
            'editor__created_at': ['date__range'],
            'editor__updated_at': ['date__range'],
        }
