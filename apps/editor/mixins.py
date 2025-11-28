from django.urls import reverse
from rest_framework import serializers
from rest_access_policy import FieldAccessMixin
from ..core import permissions, serializers as core_serializers, serializerfields as core_serializerfields
from . import models, serializerfields
from ..user import mixins as user_mixins

class EditorSerializerMixin(user_mixins.UserSerializerMixin):
    """
    This class can handle the add and modify functions of the editor model and
    return all the objects associated with this table.
    This class represents an abstract class that you can use in any app you want
    and modify the functions through inheritance operations
    """
    absolute_url = core_serializerfields.AbsoluteUrlField()
    role = serializerfields.RoleField()


    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        super(EditorSerializerMixin, self).__init__(*args, **kwargs)
        self.fields.update({
            'phone_number': serializerfields.PhoneNumberField(instance=self.instance),
        })

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        return super(EditorSerializerMixin, self).to_representation(instance)

    class Meta:
        abstract = True
        model = models.Editor
        access_policy = permissions.SafeAccountAccessPolicy
        fields = '__all__'
        read_only_fields = ('is_active', 'enabled_at', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:

        return ExampleModel.objects.create(**validated_data)
        """
        instance = self.Meta.model.objects.create_object(**validated_data)
        instance.disable()
        return instance

    def update(self, instance, validated_data):
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates, we already
        # have an instance pk for the relationships to be associated with.
        return self.Meta.model.objects.update_object(instance, **validated_data)

    def get_absolute_url(self, obj):
        """
        This function is used ro return absolute url for object
        @param obj: the custom object
        @return: url
        """
        return reverse('editor:api:editor-detail', kwargs={'pk': obj.pk})
