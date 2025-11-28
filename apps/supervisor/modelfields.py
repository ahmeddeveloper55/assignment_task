from django.conf import settings
from django.db import models

from ..core import _


class SupervisorsField(models.ManyToManyField):
    """
    M2M to the User model (admins act as supervisors).
    """
    description = _("supervisors")

    def __init__(self, *args, **kwargs):
        # must point to the User model, not member.member
        kwargs.setdefault("to", settings.AUTH_USER_MODEL)

        # explicit related_name is clearer than the %(class)ss trick
        kwargs.setdefault("related_name", "tasks_supervising")

        # keep it optional-by-default like members
        kwargs.setdefault("blank", True)
        super().__init__(*args, **kwargs)