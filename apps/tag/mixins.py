from django.urls import reverse
from rest_access_policy import FieldAccessMixin

from ..core import serializers as core_serializers, serializerfields as core_serializerfields
from . import models, permissions


class TagSerializerMixin(FieldAccessMixin, core_serializers.TranslationModelSerializer):
    """
    This class can handle the add and modify functions of the tag model and
    return all the objects associated with this table.
    This class represents an abstract class that you can use in any app you want
    and modify the functions through inheritance operations
    """
    absolute_url = core_serializerfields.AbsoluteUrlField()

    class Meta:
        abstract = True
        model = models.Tag
        access_policy = permissions.TagAccessPolicy
        fields = '__all__'
        read_only_fields = ('slug', 'is_active', 'is_active', 'enabled_at', 'created_at', 'updated_at')

    def get_absolute_url(self, obj):
        """
        This function is used ro return absolute url for object
        @param obj: the custom object
        @return: url
        """
        return reverse('tag:api:tag-detail', kwargs={'pk': obj.pk})
