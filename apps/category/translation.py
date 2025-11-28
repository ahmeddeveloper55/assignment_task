from modeltranslation.translator import register, TranslationOptions
from . import models


@register(models.Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
