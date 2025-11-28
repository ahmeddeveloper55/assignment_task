from django_filters import rest_framework as filters

from . import models


class EpisodeFilter(filters.FilterSet):
    """
    CMS filters.
    """
    class Meta:
        model = models.Episode
        fields = {
            'id': ['exact'],
            'program': ['exact'],
            'media_type': ['exact'],
            'is_published': ['exact'],
            'is_featured': ['exact'],
            'publish_date': ['date__range'],
            'created_at': ['date__range'],
            'updated_at': ['date__range'],
        }


class DiscoveryEpisodeFilter(filters.FilterSet):
    """
    Discovery filters.
    """
    class Meta:
        model = models.Episode
        fields = {
            'program__slug': ['exact'],
            'program__category__slug': ['exact'],
            'media_type': ['exact'],
            'program__language': ['exact'],
        }


EpisodeSearchFields = ('title', 'short_description', 'body')