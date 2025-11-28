from django.db import models

from ..core.utils.translation import _
from apps.episode import EpisodeMediaTypeChoices
from ..program.modelfields import UrlField
from ..core import modelfields as core_modelfields


class MediaTypeField(models.CharField):
    description = _("media type")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 20)
        kwargs.setdefault("choices", EpisodeMediaTypeChoices.choices)
        kwargs.setdefault("default", EpisodeMediaTypeChoices.AUDIO)
        super(MediaTypeField, self).__init__(*args, **kwargs)




class EpisodeNumberField(models.PositiveIntegerField):
    description = _("episode number")


class SeasonNumberField(models.PositiveIntegerField):
    description = _("season number")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        super(SeasonNumberField, self).__init__(*args, **kwargs)


class DurationSecondsField(models.PositiveIntegerField):
    description = _("duration seconds")


class PublishDateTimeField(models.DateTimeField):
    description = _("publish datetime")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        super(PublishDateTimeField, self).__init__(*args, **kwargs)


class ProgramField(models.ForeignKey):
    description = _("program")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("to", 'program.Program')
        kwargs.setdefault("on_delete", models.CASCADE)
        kwargs.setdefault("related_name", 'episodes')
        super(ProgramField, self).__init__(*args, **kwargs)


class TitleField(core_modelfields.NameField):
    description = _("episode title")


class IsPublishedField(models.BooleanField):
    description = _("is published")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("default", False)
        super(IsPublishedField, self).__init__(*args, **kwargs)


class IsFeaturedField(models.BooleanField):
    description = _("is featured")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("default", False)
        super(IsFeaturedField, self).__init__(*args, **kwargs)
