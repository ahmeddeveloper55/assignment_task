from ..core import serializerfields as core_serializerfields
from . import models


class TagField(core_serializerfields.PrimaryKeyRelatedField):
    """
    This field represents the tag field,
    as it can be used in all serializers built through Django Restfull framework.
    """
    queryset = models.Tag.activated_objects.all()

    def get_queryset(self):
        return self.queryset


class TagsField(core_serializerfields.ListField):
    """
    This field represents the tags field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault('child', TagField())
        super().__init__(**kwargs)
