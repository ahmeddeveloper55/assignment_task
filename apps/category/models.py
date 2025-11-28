from django.db import models

from ..core import _, models as core_models, modelfields as core_modelfields
from ..core.utils import slug
from . import managers
from ..core.utils.slug import slugify


class Category(core_models.CommonModel, core_models.ActivateModel, core_models.TrackedModel):

    name = core_modelfields.NameField()
    slug = core_modelfields.SlugField()


    objects = managers.BaseCategoryManager()

    class Meta:
        ordering = ['name']
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        # to slugify the title , name etc
        if not self.slug and self.name:
            self.slug = slug.slugify(self, 'name')
        super().save(*args, **kwargs)


