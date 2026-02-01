from ..core import _, serializerfields as core_serializerfields
from ..user import serializerfields as user_serializerfields, RoleChoices
from . import models, permissions


class EditorField(core_serializerfields.PrimaryKeyRelatedField):
    """
    This field represents the field for the editor field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    queryset = models.Editor.objects.none()

    def get_queryset(self):
        return permissions.EditorAccessPolicy.scope_queryset(self.request, self.queryset)



class RoleField(core_serializerfields.HiddenField):
    """
    This field represents the field for the role field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault('default', RoleChoices.EDITOR)
        super().__init__(**kwargs)