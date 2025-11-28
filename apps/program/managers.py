from django.db import transaction

from ..core import managers as core_managers
from ..core.utils import datetime, slug


class ProgramQuerySet(core_managers.BaseQuerySet):
    """
    Represent a lazy database lookup for a set of programs.
    """

    def published(self):
        return self.filter(is_published=True, publish_date__lte=datetime.now().date())

    def featured(self):
        return self.published().filter(is_featured=True)


class BaseProgramManager(core_managers.BaseManager):

    def get_queryset(self):
        return ProgramQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def featured(self):
        return self.get_queryset().featured()

