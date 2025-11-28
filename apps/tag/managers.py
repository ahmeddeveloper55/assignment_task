from ..core import managers as core_managers


class TagQueryset(core_managers.BaseQuerySet):
    """
    Represent a lazy database lookup for a set of objects.
    """


class BaseTagManager(core_managers.BaseManager):

    def get_queryset(self):
        return TagQueryset(self.model, using=self._db)
