from modeltranslation.translator import register, TranslationOptions
from . import models

@register(models.Editor)
class EditorTranslationOptions(TranslationOptions):
    fields = ('name',)
