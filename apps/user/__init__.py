from django.db import models

from ..core.utils.translation import _


class RoleChoices(models.TextChoices):
    """
    Class for creating enumerated string choices.
    """
    ADMIN = 'admin', _("Admin")
    CLIENT = 'client', _("Client")
    EDITOR = 'editor', _("Editor")


class GenderChoices(models.TextChoices):
    """
    Class for creating enumerated string choices.
    """
    MALE = 'male', _('Male')
    FEMALE = 'female', _('Female')
