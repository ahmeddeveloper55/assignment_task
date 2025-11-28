from ..core import managers as core_managers


class CategoryQuerySet(core_managers.BaseQuerySet):
    """
    Represent a lazy database lookup for categories.
    """


class BaseCategoryManager(core_managers.BaseManager):

    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)
