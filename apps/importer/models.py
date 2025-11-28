# apps/importer/models.py
from django.db import models

from ..core import _, models as core_models
from ..program import models as program_models
from ..episode import models as episode_models


class ContentSource(core_models.CommonModel):
    """
    Represents an external system or feed we importer from.
    Examples: youtube, rss, manual-upload, partner-api
    """
    SYSTEM_CHOICES = (
        ("youtube", _("YouTube")),
        ("rss", _("RSS")),
        ("manual", _("Manual")),
        ("other", _("Other")),
    )

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    system = models.CharField(max_length=20, choices=SYSTEM_CHOICES, default="manual")
    config = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = _("content source")
        verbose_name_plural = _("content sources")

    def __str__(self):
        return f"{self.name} ({self.code})"


class ImportRecord(core_models.CommonModel):
    """
    Minimal tracking for imports.

    - entity_type: "program" or "episode"
    - external_id: id in the external source (e.g. YouTube videoId, RSS guid)
    - program / episode: link to internal object, if created
    """
    PROGRAM = "program"
    EPISODE = "episode"
    ENTITY_CHOICES = (
        (PROGRAM, _("program")),
        (EPISODE, _("episode")),
    )

    SUCCESS = "success"
    FAILED = "failed"
    STATUS_CHOICES = (
        (SUCCESS, _("success")),
        (FAILED, _("failed")),
    )

    source = models.ForeignKey(ContentSource, on_delete=models.CASCADE, related_name="imports")
    entity_type = models.CharField(max_length=16, choices=ENTITY_CHOICES)
    external_id = models.CharField(max_length=255)

    program = models.ForeignKey(
        program_models.Program,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="import_records",
    )
    episode = models.ForeignKey(
        episode_models.Episode,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="import_records",
    )

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=SUCCESS)
    last_error = models.TextField(blank=True)

    class Meta:
        unique_together = ("source", "entity_type", "external_id")
        verbose_name = _("importer record")
        verbose_name_plural = _("importer records")

    def __str__(self):
        return f"{self.source.code}:{self.entity_type}:{self.external_id}"