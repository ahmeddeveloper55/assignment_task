from ..core import _, models as core_models, modelfields as core_modelfields
from ..user import modelfields as user_modelfields
from . import managers, modelfields




class Editor(core_models.CommonModel, core_models.VerifiedModel,
            core_models.TrackedModel):
    """
    This class is used to represent the editor's data within the system,
    where each editor is represented by the editor's name, the editor's image,
    and the editor's email.
    """
    name = core_modelfields.NameField()

    email = core_modelfields.EmailField()

    user = modelfields.UserField()
    
    phone_number = core_modelfields.PhoneNumberField(null=True,blank=True)

    sort_order = core_modelfields.SortOrderField()

    description = core_modelfields.DescriptionField()

    objects = managers.BaseEditorManager()
    activated_objects = managers.ActivatedEditorManager()
    disabled_objects = managers.DisabledEditorManager()
    deleted_objects = managers.DeletedEditorManager()
    undeleted_objects = managers.UndeletedEditorManager()
    verified_objects = managers.VerifiedEditorManager()

    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = _('editor')
        verbose_name_plural = _('editors')

    def __str__(self):
        """
        This method used to return string of object.
        @return: str
        """
        return f'{self.name}'

    




