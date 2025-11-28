from django_filters import rest_framework as filters
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from . import models


EditorSearchFields = ['name_en', 'name_ar']


class EditorFilter(filters.FilterSet):
    """
    This class used to filter all users based some fields and return to viewset model.
    """
    phone_number__contains = filters.CharFilter(field_name='editorusers__user__phone_number', lookup_expr='contains')

    class Meta:
        model = models.Editor
        fields = {
            'id': ['exact'],
            'name': ['contains'],
            'name_en': ['contains'],
            'name_ar': ['contains'],
            'email': ['contains'],
            'created_at': ['date__range'],
            'updated_at': ['date__range'],
        }




class EditorUserFilter(filters.FilterSet):
    """
    This class used to filter Editor user fields and return to viewset model.
    """

    class Meta:
        model = models.EditorUser
        fields = {
            'id': ['exact'],
            'user': ['exact'],
            'is_manager': ['exact'],
            'user__name': ['contains'],
            'user__username': ['contains'],
            'user__phone_number': ['contains'],
            'user__email': ['contains'],
            'user__last_login': ['date__range'],
            'created_at': ['date__range'],
            'updated_at': ['date__range'],
        }
