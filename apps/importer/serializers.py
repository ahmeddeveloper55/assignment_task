# apps/importer/serializers.py
from rest_framework import serializers

from . import models


class ContentSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContentSource
        fields = ("id", "code", "name", "system", "config")


class ImportRecordSerializer(serializers.ModelSerializer):
    source = ContentSourceSerializer()

    class Meta:
        model = models.ImportRecord
        fields = (
            "id",
            "source",
            "entity_type",
            "external_id",
            "program",
            "episode",
            "status",
            "last_error",
            "created_at",
            "updated_at",
        )


class ImportProgramSerializer(serializers.Serializer):
    """
    Payload for importing/upserting a program from an external source.
    """
    source_code = serializers.CharField(max_length=50)
    external_id = serializers.CharField(max_length=255)
    program = serializers.DictField()


class ImportEpisodeSerializer(serializers.Serializer):
    """
    Payload for importing/upserting an episode for a given program.
    """
    source_code = serializers.CharField(max_length=50)
    external_id = serializers.CharField(max_length=255)
    program_id = serializers.UUIDField()
    episode = serializers.DictField()