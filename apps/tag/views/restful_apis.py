from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters as rest_filters

from ...core import viewsets, mixins as core_mixins
from .. import models, serializers, permissions, filters


class TagViewSet(viewsets.ModelViewSet, core_mixins.ActivateModelMixin):
    """
    View for handling the tag process, It includes returning a list of all tags,
    or returning the details of only one tag.
    """
    queryset = models.Tag.objects.none()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.TagAccessPolicy,)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.TagFilter
