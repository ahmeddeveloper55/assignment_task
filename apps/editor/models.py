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

    def users(self):
        """
        This method is used to return users for owner.
        """
        return self.editorusers.all()

    def manager(self):
        """
        This method is used to return users for owner.
        """
        return getattr(self.users().first(), 'user', None)



    def active(self):
        """
        this method is used to active object.
        """
        [editoruser.user.active() for editoruser in self.users()]
        return super(Editor, self).active()

    def disable(self):
        """
        this method is used to disable object.
        """
        [editoruser.user.disable() for editoruser in self.users()]
        return super(Editor, self).disable()

    def update(self, **kwargs):
        """
        This function is used to update the instance data, as it will facilitate
        the modification of the instance data without making a new query
        """
        if 'image' in kwargs.keys() and not kwargs['image']:
            kwargs.pop('image')

        if 'core' in kwargs.keys() and not kwargs['core']:
            kwargs.pop('core')

        return super(Editor, self).update(**kwargs)

    def delete(self):
        """
        This method deletes user data from the database.
        """
        [editoruser.user.hard_delete() for editoruser in self.users()]
        return self.hard_delete()

    @property
    def phone_number(self):
        """
        This method is used to return the phone number of the editor.
        """
        return getattr(self.manager(), "phone_number", None)


class EditorUser(core_models.CommonModel):
    """
    This class is used to linked users with editor, where each editor can have
    more than one user in the system.
    """
    is_manager = modelfields.IsManagerField()

    user = user_modelfields.UserOneToOneField()

    editor = modelfields.EditorField()

    objects = managers.BaseEditorUserManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('editor_user')
        verbose_name_plural = _('editor_users')

    def __str__(self):
        """
        This method used to return string of object.
        @return: str
        """
        return f'{self.user.__str__()}'

    def active(self):
        """
        this method is used to active object.
        """
        active = getattr(self.user, 'active')
        return active()

    def disable(self):
        """
        this method is used to disable object.
        """
        disable = getattr(self.user, 'disable')
        return disable()

    def delete(self, **kwargs):
        """
        This method deletes user data from the database.
        """
        user = getattr(self, 'user', None)

        if user is None:
            return super(EditorUser, self).delete()

        if hasattr(user, 'hard_delete'):
            user.hard_delete()
        else:
            user.delete()
