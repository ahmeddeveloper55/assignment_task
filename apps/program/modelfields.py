from django.conf import settings
from django.db import models

from ..core import _, modelfields as core_modelfields
from . import ProgramTypeChoices, EpisodeMediaTypeChoices


class TitleField(core_modelfields.NameField):
    description = _("title")


class ShortDescriptionField(models.CharField):
    description = _("short description")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 500)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        super(ShortDescriptionField, self).__init__(*args, **kwargs)


class LongDescriptionField(core_modelfields.DescriptionField):
    description = _("long description")


class ProgramTypeField(models.CharField):
    description = _("type")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 50)
        kwargs.setdefault("choices", ProgramTypeChoices.choices)
        kwargs.setdefault("default", ProgramTypeChoices.PODCAST)
        super(ProgramTypeField, self).__init__(*args, **kwargs)


class LanguageField(models.CharField):
    description = _("language")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 10)
        kwargs.setdefault("choices", settings.LANGUAGES)
        kwargs.setdefault("default", settings.LANGUAGE_CODE)
        super(LanguageField, self).__init__(*args, **kwargs)


class UrlField(models.URLField):
    description = _("url")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        super(UrlField, self).__init__(*args, **kwargs)


class ColorField(models.CharField):
    description = _("accent color")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 20)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        super(ColorField, self).__init__(*args, **kwargs)


class PublishDateField(models.DateField):
    description = _("publish date")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        super(PublishDateField, self).__init__(*args, **kwargs)


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


class CategoryField(models.ForeignKey):
    description = _("category")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("to", 'program_category.Category')
        kwargs.setdefault("on_delete", models.SET_NULL)
        kwargs.setdefault("null", True)
        kwargs.setdefault("related_name", 'programs')
        super(CategoryField, self).__init__(*args, **kwargs)


class EpisodeField(models.ForeignKey):
    description = _("episode")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("to", 'episode.Episode')
        kwargs.setdefault("on_delete", models.CASCADE)
        kwargs.setdefault("related_name", 'links')
        super(EpisodeField, self).__init__(*args, **kwargs)
