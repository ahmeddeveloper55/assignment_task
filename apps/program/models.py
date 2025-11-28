from django.db import models
from django.utils import timezone

from ..core import _, models as core_models, modelfields as core_modelfields
from ..core.utils import slug
from ..category import models as category_models
from ..core.utils.slug import slugify
from ..tag import models as tag_models
from ..tag import modelfields as tag_modelfields
from . import ProgramTypeChoices, managers, modelfields


class Program(core_models.CommonModel, core_models.TrackedModel, core_models.ActivateModel):
    title = modelfields.TitleField()
    slug = core_modelfields.SlugField(unique=True)
    short_description = modelfields.ShortDescriptionField(blank=True)
    long_description = modelfields.LongDescriptionField(blank=True)
    category = models.ForeignKey(
        category_models.Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='programs'
    )
    type = modelfields.ProgramTypeField()
    language = modelfields.LanguageField()
    cover_image_url = core_modelfields.UrlField(max_length=1000)
    accent_color = modelfields.ColorField()
    publish_date = modelfields.PublishDateField()
    is_published = modelfields.IsPublishedField()
    is_featured = modelfields.IsFeaturedField()
    episodes_count = models.PositiveIntegerField(default=0)
    tags = tag_modelfields.TagsField(blank=True)

    objects = managers.BaseProgramManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('program')
        verbose_name_plural = _('programs')

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slug.slugify(self, 'title')
        super().save(*args, **kwargs)
