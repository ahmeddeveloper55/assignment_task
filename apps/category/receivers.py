from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models

"""
 ============================================================== 
     Django Receiver for Notification
 ============================================================== 
"""


@receiver(post_save, sender=models.Category)
def create_category_notification(sender, instance, created, **kwargs):
    pass

