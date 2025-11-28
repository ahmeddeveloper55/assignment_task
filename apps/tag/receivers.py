from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models

"""
 ============================================================== 
     Django Receiver for Notification
 ============================================================== 
"""


@receiver(post_save, sender=models.Tag)
def receiver_tag_created(sender, instance, created, *args, **kwargs):
    pass
