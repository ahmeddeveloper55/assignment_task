from django_filters import rest_framework as filters

from . import models


class ProgramFilter(filters.FilterSet):
    """
    CMS filters.
    """
    class Meta:
        model = models.Program
        fields = {
            'id': ['exact'],
            'title': ['icontains'],
            'slug': ['exact'],
            'category': ['exact'],
            'type': ['exact'],
            'language': ['exact'],
            'is_published': ['exact'],
            'is_featured': ['exact'],
            'publish_date': ['range'],
            'created_at': ['date__range'],
            'updated_at': ['date__range'],
        }


class DiscoveryProgramFilter(filters.FilterSet):
    """
    Discovery filters.
    """
    class Meta:
        model = models.Program
        fields = {
            'category__slug': ['exact'],
            'type': ['exact'],
            'language': ['exact'],
            'is_featured': ['exact'],
        }


ProgramSearchFields = ('title', 'short_description')