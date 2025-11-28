from ..core import serializerfields as core_serializerfields
from ..user import RoleChoices
from . import models


class CurrentClientDefault:
    """
    This class used to return hotel object form http request
    """
    requires_context = True

    def __call__(self, serializer_field):
        """
        method enables Python programmers to write classes where the instances
        behave like functions and can be called like a function.
        :return: user object
        """
        request = serializer_field.context.get('request', None)
        if request is not None:
            user = getattr(request, 'user', None)
            if user is not None and user.is_client:
                return user.client
        return None

    def __repr__(self):
        """
        special methods are a set of predefined methods used to enrich your classes.
        They start and end with double underscores.
        :return:
        """
        return '%s()' % self.__class__.__name__




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
        kwargs.setdefault('default', RoleChoices.CLIENT)
        super().__init__(**kwargs)





class ClientField(core_serializerfields.PrimaryKeyRelatedField):
    """
    This field represents the field for the client field,
    as it can be used in all serializers built through Django Restfull framework.
    """
    queryset = models.Client.objects.none()

    def get_queryset(self):
        return models.Client.objects.all()

    def get_value(self, dictionary):
        # We always use the default value for `HiddenField`.
        # User input is never provided or accepted.
        if self.user.is_client:
            return getattr(CurrentClientDefault()(self), 'pk', None)

        return super(ClientField, self).get_value(dictionary)
