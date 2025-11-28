from django.urls import reverse
from rest_access_policy import FieldAccessMixin
from rest_framework import serializers

from ..core import serializers as core_serializers
from ..core import serializerfields as core_serializersfields
from ..tag import models as tag_models
from ..tag import serializerfields as tag_serializerfields
from ..category import serializerfields as category_serializerfields
from . import models, permissions


class ProgramSerializerMixin(FieldAccessMixin, core_serializers.ModelSerializer):
    """
    All behavior for Program serializers (CMS + Discovery) lives here.
    """
    absolute_url = core_serializersfields.AbsoluteUrlField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    category_id = category_serializerfields.CategoryField(
        source='category',
        write_only=True,
        required=True
    )
    tags = tag_serializerfields.TagField(many=True, required=False)
    class Meta:
        abstract = True
        model = models.Program
        access_policy = permissions.ProgramAccessPolicy
        fields = '__all__'
        read_only_fields = ('id','slug', 'episodes_count','is_active','enabled_at', 'created_at', 'updated_at', 'created_by', 'updated_by')

    

    def get_absolute_url(self, obj):
        return reverse('program:api:program-detail', kwargs={'pk': obj.pk})