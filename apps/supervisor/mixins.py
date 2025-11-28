from django.urls import reverse

from ..core import serializerfields as core_serializerfields
from ..user import mixins as user_mixins
from . import serializerfields


class SupervisorSerializerMixin(user_mixins.UserSerializerMixin):
    """
    This class can handle the add and modify functions of the user model and
    return all the objects associated with this table.
    This class represents an abstract class that you can use in any app you want
    and modify the functions through inheritance operations
    """

    role = serializerfields.RoleField()

    absolute_url = core_serializerfields.AbsoluteUrlField()

    def get_absolute_url(self, obj):
        """
        This function is used ro return absolute url for object
        @param obj: the custom object
        @return: url
        """
        return reverse('supervisor:api:supervisor-detail', kwargs={'pk': obj.pk})
