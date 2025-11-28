from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters

from ...core import viewsets, mixins as core_mixins
from .. import models, serializers, permissions, filters


class CategoryViewSet(viewsets.ModelViewSet, core_mixins.ActivateModelMixin):
    queryset = models.Category.objects.none()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.CategoryAccessPolicy,)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.CategoryFilter
    search_fields = filters.CategorySearchFields