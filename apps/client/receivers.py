from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models
from ..core.decorators import disable_for_fixture

"""
 ==============================================================
     Django Receiver for DB
 ==============================================================
"""

USER_MODEL = get_user_model()


@receiver(post_save, sender=USER_MODEL)
@disable_for_fixture
def receiver_create_client(sender, instance, created, *args, **kwargs):
    if not created or not instance.is_client:
        return

    client = models.Client.objects.create(user=instance, created_by=instance.created_by)
    return client


@receiver(post_save, sender=models.Client)
def receiver_client_created(sender, instance, created, *args, **kwargs):
    pass
