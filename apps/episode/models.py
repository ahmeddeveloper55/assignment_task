from django.db import models
from django.utils import timezone

from ..core import _, models as core_models, modelfields as core_modelfields
from ..core.utils import slug
from ..core.utils.slug import slugify
from ..program import EpisodeMediaTypeChoices
from ..program import modelfields as program_modelfields

from ..tag import models as tag_models
from ..tag import modelfields as tag_modelfields
from . import managers,modelfields


class Episode(core_models.CommonModel, core_models.TrackedModel,core_models.ActivateModel):
    program = modelfields.ProgramField()
    title = modelfields.TitleField()
    slug = core_modelfields.SlugField()
    short_description = program_modelfields.ShortDescriptionField()
    body = core_modelfields.DescriptionField()
    publish_date = modelfields.PublishDateTimeField()
    duration_seconds = modelfields.DurationSecondsField()
    episode_number = modelfields.EpisodeNumberField()
    season_number = modelfields.SeasonNumberField()
    thumbnail_url = program_modelfields.UrlField()
    media_type = modelfields.MediaTypeField()
    media_url = core_modelfields.UrlField(max_length=1000)
    is_published = modelfields.IsPublishedField()
    is_featured = modelfields.IsFeaturedField()
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=512, blank=True)

    tags = tag_modelfields.TagsField(blank=True)

    objects = managers.BaseEpisodeManager()

    class Meta:
        ordering = ['-publish_date']
        verbose_name = _('episode')
        verbose_name_plural = _('episodes')

    def __str__(self):
        return f'{self.program.title} – {self.title}'
    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slug.slugify(self, 'title')
        super().save(*args, **kwargs)


class EpisodeLink(core_models.CommonModel):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='links')
    label = modelfields.TitleField()
    url = program_modelfields.UrlField()
    sort_order = core_modelfields.SortOrderField()

    class Meta:
        ordering = ['sort_order']
        verbose_name = _('episode link')
        verbose_name_plural = _('episode links')

    def __str__(self):
        return f"{self.label}"
