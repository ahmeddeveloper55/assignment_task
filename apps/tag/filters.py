from django_filters import rest_framework as filters

from . import models


class TagFilter(filters.FilterSet):
    """
    This class used to filter tag fields and return to viewset model.
    """
    class Meta:
        model = models.Tag
        fields = {
            'id': ['exact'],
            'name': ['contains'],
            'name_en': ['contains'],
            'name_ar': ['contains'],
            'created_at': ['date__range'],
            'updated_at': ['date__range'],
        }
