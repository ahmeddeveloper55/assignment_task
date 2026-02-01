from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models

"""
 ==============================================================
     Django Receiver for DB
 ==============================================================
"""


@receiver(post_save, sender=models.Editor)
def receiver_editor_created(sender, instance, created, *args, **kwargs):
    pass
