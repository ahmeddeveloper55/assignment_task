from . import mixins


class ClientSerializer(mixins.ClientSerializerMixin):
    """
    This class can handle the add and modify functions of the user model and
    return all the objects associated with this table.
    This class represents an abstract class that you can use in any app you want
    and modify the functions through inheritance operations
    """
