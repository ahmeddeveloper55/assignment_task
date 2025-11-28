from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models

"""
 ==============================================================
     Django Receiver for DB
 ==============================================================
"""


@receiver(post_save, sender=models.Editor)
def receiver_owner_created(sender, instance, created, *args, **kwargs):
    pass


@receiver(post_save, sender=models.EditorUser)
def receiver_owner_user_created(sender, instance, created, *args, **kwargs):
    pass
