from rest_access_policy import FieldAccessMixin

from ..core import serializers as core_serializers
from . import models, permissions, mixins


class CategorySerializer(mixins.CategorySerializerMixin):
    """
    Plain serializer. All behavior is inside the mixin.
    """
    pass



