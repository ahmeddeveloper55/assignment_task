from django.dispatch import receiver
from django.contrib.auth import get_user_model

from ..core.decorators import disable_for_fixture
from ..core.utils import datetime
from . import signals

UserModel = get_user_model()

"""
 ==============================================================
     Django Receiver for DB
 ==============================================================
"""


@receiver(signals.user_logging)
@disable_for_fixture
def receiver_user_logging(sender, user, **kwargs):
    user.last_login = datetime.now()
    user.save()
