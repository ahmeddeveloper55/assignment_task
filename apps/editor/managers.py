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

