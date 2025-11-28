from django.db import models

from ..core.utils.translation import _


class ProgramTypeChoices(models.TextChoices):
    PODCAST = 'podcast', _('Podcast')
    DOCUMENTARY = 'documentary', _('Documentary')
    SHOW = 'show', _('Show')
    OTHER = 'other', _('Other')


class EpisodeMediaTypeChoices(models.TextChoices):
    AUDIO = 'audio', _('Audio')
    VIDEO = 'video', _('Video')


class SearchEntityChoices(models.TextChoices):
    PROGRAM = 'program', _('Program')
    EPISODE = 'episode', _('Episode')
