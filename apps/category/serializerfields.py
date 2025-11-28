# apps/category/serializerfields.py
from ..core import serializerfields as core_serializerfields
from . import models, permissions


class CategoryField(core_serializerfields.PrimaryKeyRelatedField):
    """
    Reusable field for Category FKs.
    Uses access policy to scope queryset per request/user.
    """

    queryset = models.Category.objects.none()

    def get_queryset(self):
        # rest_access_policy passes request into the field instance
        return permissions.CategoryAccessPolicy.scope_queryset(self.request, self.queryset)


class CategoriesField(core_serializerfields.ListField):
    """
    If you ever need a list of categories.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('child', CategoryField())
        super().__init__(**kwargs)