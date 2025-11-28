from ..core import serializerfields as core_serializerfields
from ..user import RoleChoices
from django.contrib.auth import get_user_model



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
        kwargs.setdefault('default', RoleChoices.ADMIN)
        super().__init__(**kwargs)


class SupervisorsField(core_serializerfields.PrimaryKeyRelatedField):
    """
    Accept a list of supervisor IDs (Users with admin role).
    """
    def __init__(self, **kwargs):
        User = get_user_model()
        kwargs.setdefault("many", True)
        kwargs.setdefault("queryset", User.objects.filter(role=RoleChoices.ADMIN))
        super().__init__(**kwargs)
