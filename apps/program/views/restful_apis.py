from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters

from ...core import viewsets, mixins as core_mixins
from .. import models, serializers, permissions, filters


class ProgramViewSet(viewsets.ModelViewSet, core_mixins.ActivateModelMixin):
    """
    CMS CRUD for programs.
    """
    queryset = models.Program.objects.none()
    serializer_class = serializers.ProgramSerializer
    permission_classes = (permissions.ProgramAccessPolicy,)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.ProgramFilter
    search_fields = filters.ProgramSearchFields

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        # search indexing handled by receiver_program_saved

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
        # search indexing handled by receiver_program_saved

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        # receiver_program_saved will see is_active=False and remove from search


class DiscoveryProgramViewSet(viewsets.ReadOnlyModelViewSet,core_mixins.CachedViewSetMixin):
    """
    Discovery programs.
    """
    cache_timeout = 24 * 60 * 60
    queryset = models.Program.objects.none()
    serializer_class = serializers.ProgramSerializer
    permission_classes = (permissions.DiscoveryAccessPolicy,)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.DiscoveryProgramFilter
    search_fields = filters.ProgramSearchFields