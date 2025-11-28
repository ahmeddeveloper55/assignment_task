from django.contrib.auth import get_user_model
from django.db.models import Count, F
from django.utils.translation import get_language

from ..core import managers as core_managers

UserModel = get_user_model()



class EditorQueryset(core_managers.BaseQuerySet):
    """
    Represent a lazy database lookup for a set of objects.
    """



class BaseEditorManager(core_managers.BaseManager):

    def get_queryset(self):
        return EditorQueryset(self.model, using=self._db)


    def create_object(self, **kwargs):
        """
        This method is used to create instance of editor and return this instance.
        @return editor
        """
        phone_number = kwargs.pop('phone_number')
      

        editor = self.create(**kwargs)

        user = UserModel.objects.create_editor(phone_number=phone_number, name=editor.name, email=editor.email)
        user.profile.update(**kwargs)

        editor.editorusers.create(user=user, is_manager=True)

        return editor

    def update_object(self, editor, **kwargs):
        """
        This method is used to update instance of editor and return this instance.
        @return reservation
        """
        user = editor.manager()

        phone_number = kwargs.pop('phone_number', user.phone_number)
        editor.update(**kwargs)
        user.update(phone_number=phone_number, **kwargs)
        user.profile.update(**kwargs)
        return editor


class ActivatedEditorManager(BaseEditorManager):

    def get_queryset(self):
        return EditorQueryset(self.model, using=self._db).filter(is_active=True)


class DisabledEditorManager(BaseEditorManager):

    def get_queryset(self):
        return EditorQueryset(self.model, using=self._db).filter(is_active=False)


class DeletedEditorManager(BaseEditorManager):

    def get_queryset(self):
        return EditorQueryset(self.model, using=self._db).filter(is_deleted=True)


class UndeletedEditorManager(BaseEditorManager):

    def get_queryset(self):
        return EditorQueryset(self.model, using=self._db).filter(is_deleted=False)


class VerifiedEditorManager(BaseEditorManager):

    def get_queryset(self):
        return EditorQueryset(self.model, using=self._db).filter(is_active=True, is_deleted=False)


class EditorUserQueryset(core_managers.BaseQuerySet):
    """
    Represent a lazy database lookup for a set of objects.
    """

    def find_by_editor(self, editor, **filter):
        """
        This function is used to return all users associated with the editor passed through
        the editor variable.
        """
        return self.filter(editor=editor, **filter)

    def managers(self, **filter):
        """
        This function is used to return all managers for editor.
        """

        return self.filter(is_manager=True, **filter)

    def users(self, **filter):
        """
        This function is used to return all users for editor.
        """

        return self.filter(is_manager=False, **filter)


class BaseEditorUserManager(core_managers.BaseManager):

    def get_queryset(self):
        return EditorUserQueryset(self.model, using=self._db)

    def find_by_editor(self, editor, **filter):
        """
        This function is used to return all users associated with the editor passed through
        the editor variable.
        """
        filter.update({'editor': editor})
        return self.get_queryset().find_by_editor(**filter)

    def managers(self, **filter):
        """
        This function is used to return all managers for editor.
        """

        return self.get_queryset().managers(**filter)

    def users(self, **filter):
        """
        This function is used to return all user for editor.
        """

        return self.get_queryset().users(**filter)

    def create_manager(self, user, editor, **kwargs):
        """
        Create editor user by passing user and editor objects.
        @:param editor: this is the editor object.
        @:param user:  this is the user object.
        @:returns new editor user
        """

        kwargs.setdefault("editor", editor)
        kwargs.setdefault("is_manager", True)
        return self.update_or_create(user=user, defaults=kwargs)

    def create_user(self, user, editor, **kwargs):
        """
        Create editor user by passing user and editor objects.
        @:param editor: this is the editor object.
        @:param user:  this is the user object.
        @:returns new editor user
        """

        kwargs.setdefault("editor", editor)
        return self.update_or_create(user=user, defaults=kwargs)
