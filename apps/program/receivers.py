# apps/program/receivers.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from . import models
from ..search.services import SearchService

@receiver(post_save, sender=models.Program)
def receiver_program_saved(sender, instance: models.Program, created, **kwargs):
    """
    When a program is created or updated:
      - If active & published, index it.
      - Otherwise, remove it from search.
    """
    if instance.is_active and instance.is_published:
        SearchService.index_program(instance)
    else:
        SearchService.remove_program(instance.id)


@receiver(post_delete, sender=models.Program)
def receiver_program_deleted(sender, instance: models.Program, **kwargs):
    """
    When a program is hard-deleted:
      - Remove it from search index.
    """
    SearchService.remove_program(instance.id)