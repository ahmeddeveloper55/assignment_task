import django_otp
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from ..core.decorators import disable_for_fixture
from . import models

UserModel = get_user_model()

"""
 ==============================================================
     Django Receiver for DB
 ==============================================================
"""


@receiver(post_save, sender=UserModel)
@disable_for_fixture
def receiver_create_profile(sender, instance, created, **kwargs):
    if not created:
        return

    profile = models.Profile.objects.create(user=instance)
    return profile


@receiver(post_save, sender=UserModel)
@disable_for_fixture
def receiver_update_device(sender, instance, created, **kwargs):
    """
    This method is used to update device phone number
    """
    if created is True:
        return

    for device in django_otp.devices_for_user(instance):
        device.number = instance.phone_number
        device.save()

    return instance
