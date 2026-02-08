from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters as rest_filters

from ...core import viewsets, mixins as core_mixins
from .. import models, serializers, permissions, filters


class TagViewSet(viewsets.ModelViewSet, core_mixins.ActivateModelMixin):
    """
    CMS CRUD for tags.
    """
    queryset = models.Tag.objects.none()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.TagAccessPolicy,)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.TagFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """
        Soft delete and deactivate the tag.
        """
        instance.delete()  # Sets is_deleted=True
        instance.is_active = False
        instance.save(update_fields=['is_active'])
