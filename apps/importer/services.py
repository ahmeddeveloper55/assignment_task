# apps/importer/services.py
from django.db import transaction

from . import models
from ..program import models as program_models
from ..program.serializers import ProgramSerializer
from ..episode import models as episode_models
from ..episode.serializers import EpisodeSerializer


class ImportService:
    """
    Small, synchronous service that reuses Program/Episode serializers.
    Idempotent per (source_code, external_id, entity_type).
    """

    @staticmethod
    @transaction.atomic
    def import_program(*, source_code: str, external_id: str, program_data: dict, request):
        source, _ = models.ContentSource.objects.get_or_create(
            code=source_code,
            defaults={"name": source_code, "system": "other"},
        )

        record, _ = models.ImportRecord.objects.get_or_create(
            source=source,
            entity_type=models.ImportRecord.PROGRAM,
            external_id=external_id,
        )

        if record.program:
            instance = record.program
            serializer = ProgramSerializer(
                instance=instance,
                data=program_data,
                partial=True,
                context={"request": request},
            )
        else:
            serializer = ProgramSerializer(
                data=program_data,
                context={"request": request},
            )

        serializer.is_valid(raise_exception=True)

        if record.program:
            program = serializer.save(updated_by=getattr(request, "user", None))
        else:
            program = serializer.save(created_by=getattr(request, "user", None))

        record.program = program
        record.status = models.ImportRecord.SUCCESS
        record.last_error = ""
        record.save(update_fields=["program", "status", "last_error"])

        return program

    @staticmethod
    @transaction.atomic
    def import_episode(
        *,
        source_code: str,
        external_id: str,
        program_id,
        episode_data: dict,
        request,
    ):
        source, _ = models.ContentSource.objects.get_or_create(
            code=source_code,
            defaults={"name": source_code, "system": "other"},
        )

        record, _ = models.ImportRecord.objects.get_or_create(
            source=source,
            entity_type=models.ImportRecord.EPISODE,
            external_id=external_id,
        )

        # Make sure the episode data targets the given program
        episode_data = dict(episode_data)  # shallow copy
        episode_data["program"] = str(program_id)

        if record.episode:
            instance = record.episode
            serializer = EpisodeSerializer(
                instance=instance,
                data=episode_data,
                partial=True,
                context={"request": request},
            )
        else:
            serializer = EpisodeSerializer(
                data=episode_data,
                context={"request": request},
            )

        serializer.is_valid(raise_exception=True)

        if record.episode:
            episode = serializer.save(updated_by=getattr(request, "user", None))
        else:
            episode = serializer.save(created_by=getattr(request, "user", None))

        record.episode = episode
        record.status = models.ImportRecord.SUCCESS
        record.last_error = ""
        record.save(update_fields=["episode", "status", "last_error"])

        return episode