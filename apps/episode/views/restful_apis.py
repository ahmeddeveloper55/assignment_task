from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters

from ...core import viewsets, mixins as core_mixins
from .. import models, serializers, permissions, filters


class EpisodeViewSet(viewsets.ModelViewSet, core_mixins.ActivateModelMixin):
    """
    CMS CRUD for episodes.
    """
    queryset = models.Episode.objects.select_related('program').prefetch_related('tags').none()
    serializer_class = serializers.EpisodeSerializer
    permission_classes = (permissions.EpisodeAccessPolicy,)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.EpisodeFilter
    search_fields = filters.EpisodeSearchFields

    def perform_create(self, serializer):
        # Signals will handle episodes_count + search sync
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()  # SoftDeleteModel.delete() handles soft-deletion


class PublicEpisodeViewSet(viewsets.ReadOnlyModelViewSet,core_mixins.CachedViewSetMixin):
    """
    Discovery episodes.
    """
    cache_timeout = 24 * 60 * 60
    queryset = models.Episode.objects.select_related('program','program__category').prefetch_related('tags','links').none()
    serializer_class = serializers.EpisodeSerializer
    permission_classes = (permissions.DiscoveryEpisodeAccessPolicy,)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    filterset_class = filters.DiscoveryEpisodeFilter
    search_fields = filters.EpisodeSearchFields

    def retrieve(self, request, *args, **kwargs):
        """
        Add previous/next episode ids for UX.
        """
        response = super().retrieve(request, *args, **kwargs)
        episode = self.get_object()

        qs = self.get_queryset().filter(program=episode.program)
        prev_episode = qs.filter(publish_date__lt=episode.publish_date).order_by('-publish_date').first()
        next_episode = qs.filter(publish_date__gt=episode.publish_date).order_by('publish_date').first()

        data = response.data
        data['previous_episode_id'] = getattr(prev_episode, 'id', None)
        data['next_episode_id'] = getattr(next_episode, 'id', None)
        response.data = data
        return response