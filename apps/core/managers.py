from django.db import models
from django_softdelete.models import SoftDeleteQuerySet, DeletedQuerySet

from .utils import datetime


class BaseQuerySet(models.QuerySet):
    """
    Represent a lazy database lookup for a set of objects.
    """


class BaseManager(models.Manager):
    #: If set to True the manager will be serialized into migrations and will
    #: thus be available in e.g. RunPython operations.
    use_in_migrations = False


class ActivatedQuerySet(BaseQuerySet):

    def disable(self):
        """
        This function modifies the value of the is_active field from true to false
        and also the value of the enabled_at field to None.
        These modifications will be executed on all queries returned from the manager class.
        """
        return self.update(is_active=False, enabled_at=None)


class DisabledQuerySet(BaseQuerySet):

    def active(self):
        """
        This function modifies the value of the is_active field from false to true
        and also the value of the enabled_at field to today date value.
        These modifications will be executed on all queries returned from the manager class.
        """
        return self.update(is_active=True, enabled_at=datetime.now())


class ActivatedManager(BaseManager):

    def get_queryset(self):
        return ActivatedQuerySet(self.model, using=self._db).filter(is_active=True)


class DisabledManager(BaseManager):

    def get_queryset(self):
        return DisabledQuerySet(self.model, using=self._db).filter(is_active=False)


class DeletedManager(BaseManager):

    def get_queryset(self):
        return DeletedQuerySet(self.model, using=self._db).filter(is_deleted=True)


class UndeletedManager(BaseManager):

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class VerifiedManager(BaseManager):

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_active=True, is_deleted=False)
