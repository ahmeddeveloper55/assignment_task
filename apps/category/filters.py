from django_filters import rest_framework as filters

from . import models


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = models.Category
        fields = {
            'id': ['exact'],
            'slug': ['exact'],
            'name': ['icontains'],
            'created_at': ['date__range'],
            'updated_at': ['date__range'],
        }
CategorySearchFields = ('name', 'slug')