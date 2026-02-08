from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters

from ...core import viewsets, mixins as core_mixins
from .. import models, serializers, permissions, filters


class CategoryViewSet(viewsets.ModelViewSet, core_mixins.ActivateModelMixin):
    """
    CMS CRUD for categories.
    """
    queryset = models.Category.objects.none()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.CategoryAccessPolicy,)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.CategoryFilter
    search_fields = filters.CategorySearchFields

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """
        Soft delete and deactivate the category.
        """
        instance.delete()  # Sets is_deleted=True
        instance.is_active = False
        instance.save(update_fields=['is_active'])