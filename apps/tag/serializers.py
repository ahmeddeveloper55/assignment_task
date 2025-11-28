from . import mixins


class TagSerializer(mixins.TagSerializerMixin):
    """
    Class handle the add and modify functions of the tag model and
    return all the objects associated with this table.
    This class represents an abstract class that you can use in any app you want
    and modify the functions through inheritance operations
    """