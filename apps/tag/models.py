from ..core import _, models as core_models, modelfields as core_modelfields
from . import managers


class Tag(core_models.CommonModel, core_models.ActivateModel,  core_models.TrackedModel):
    """
    This class is used to represent the tag data within the system,
    where each tag is represented by the tag name.
    """
    name = core_modelfields.NameField()

    note = core_modelfields.NoteField()

    objects = managers.BaseTagManager()

    class Meta:
        ordering = ['-id']
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        """
        This method used to return string of object.
        @return: str
        """
        return f'{self.name}'
