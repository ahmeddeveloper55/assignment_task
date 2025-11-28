
from . import models, permissions
from django.urls import reverse
from rest_access_policy import FieldAccessMixin
from ..core import serializers as core_serializers
from ..core import serializerfields as core_serializersfields


class CategorySerializerMixin(FieldAccessMixin, core_serializers.TranslationModelSerializer):
    """
    Mixin to add common functionality for Category serializers.
    """
    absolute_url = core_serializersfields.AbsoluteUrlField()

    class Meta:
        abstract = True
        model = models.Category
        access_policy = permissions.CategoryAccessPolicy
        fields = '__all__'
        read_only_fields = ('id','slug', 'is_active', 'enabled_at', 'created_at', 'updated_at')
        
    def get_absolute_url(self, obj):
        """
        Returns the absolute URL for the category object.
        @param obj: the category object
        @return: url
        """
        return reverse('category:api:category-detail', kwargs={'pk': obj.pk})
