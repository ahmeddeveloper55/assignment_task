# apps/episode/receivers.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from . import models
from ..program.models import Program
from ..search.services import SearchService


def _recompute_program_episodes_count(program: Program) -> None:
    """
    Keep Program.episodes_count always in sync with active episodes.
    """
    program.episodes_count = program.episodes.filter(is_active=True).count()
    program.save(update_fields=["episodes_count"])


@receiver(post_save, sender=models.Episode)
def receiver_episode_saved(sender, instance: models.Episode, created, **kwargs):
    """
    Whenever an episode is created or updated:
      - Recompute program.episodes_count
      - Update search index (or remove if not active/published)
    """
    program = instance.program
    _recompute_program_episodes_count(program)

    if instance.is_active and instance.is_published:
        SearchService.index_episode(instance)
    else:
        SearchService.remove_episode(instance.id)


@receiver(post_delete, sender=models.Episode)
def receiver_episode_deleted(sender, instance: models.Episode, **kwargs):
    """
    When an episode is hard-deleted:
      - Recompute program.episodes_count
      - Remove from search index
    """
    program = instance.program
    _recompute_program_episodes_count(program)
    SearchService.remove_episode(instance.id)