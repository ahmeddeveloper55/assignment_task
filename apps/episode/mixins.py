from django.urls import reverse
from rest_access_policy import FieldAccessMixin

from ..core import serializers as core_serializers, serializerfields as core_serializerfields
from ..tag import serializerfields as tag_serializerfields
from . import models, permissions


class EpisodeLinkSerializer(core_serializers.TranslationModelSerializer):
    class Meta:
        model = models.EpisodeLink
        fields = ('id', 'label', 'url')


class EpisodeSerializerMixin(FieldAccessMixin, core_serializers.TranslationModelSerializer):
    """
    Base serializer for Episode.
    """
    absolute_url = core_serializerfields.AbsoluteUrlField()
    tags = tag_serializerfields.TagField(many=True, required=False)
    links = EpisodeLinkSerializer(many=True, required=False)

    class Meta:
        abstract = True
        model = models.Episode
        access_policy = permissions.EpisodeAccessPolicy
        fields = '__all__'
        read_only_fields = (
            'id',
            'slug',
            'is_active',
            'enabled_at',
            'created_at',
            'updated_at',
        )

    def get_absolute_url(self, obj):
        return reverse('episode:api:episode-detail', kwargs={'pk': obj.pk})

    def create(self, validated_data):
        links_data = validated_data.pop('links', [])
        episode = super().create(validated_data)
        self._save_links(episode, links_data)
        return episode

    def update(self, instance, validated_data):
        links_data = validated_data.pop('links', None)
        episode = super().update(instance, validated_data)
        if links_data is not None:
            episode.links.all().delete()
            self._save_links(episode, links_data)
        return episode

    def _save_links(self, episode, links_data):
        if not links_data:
            return
        models.EpisodeLink.objects.bulk_create(
            [models.EpisodeLink(episode=episode, **link) for link in links_data]
        )