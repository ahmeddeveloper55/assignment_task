from django.db import transaction

from ..core import managers as core_managers
from ..core.utils import datetime, slug


class EpisodeQuerySet(core_managers.BaseQuerySet):
    """
    Represent a lazy database lookup for a set of episodes.
    """

    def published(self):
        return self.filter(is_published=True, publish_date__lte=datetime.now())

    def for_program(self, program):
        return self.filter(program=program)


class BaseEpisodeManager(core_managers.BaseManager):

    def get_queryset(self):
        return EpisodeQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def for_program(self, program):
        return self.get_queryset().for_program(program)

