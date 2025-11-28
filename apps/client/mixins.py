from django.urls import reverse
from rest_framework import serializers
from ..core import serializerfields as core_serializerfields
from ..user import mixins as user_mixins
from . import serializerfields

class ClientSerializerMixin(user_mixins.UserSerializerMixin):
    """
    This class can handle the add and modify functions of the user model and
    return all the objects associated with this table.
    This class represents an abstract class that you can use in any app you want
    and modify the functions through inheritance operations
    """
    role = serializerfields.RoleField()




    absolute_url = core_serializerfields.AbsoluteUrlField()

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        self.fields.update({
            'country': serializers.CharField(source='client.city.get_country_display', read_only=True),
            'city': serializers.CharField(source='client.city.name', read_only=True),
        })
        return super(ClientSerializerMixin, self).to_representation(instance)

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:

        return ExampleModel.objects.create(**validated_data)
        """
        instance = super(ClientSerializerMixin, self).create(validated_data)
        return instance

    def update(self, instance, validated_data):
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates, we already
        # have an instance pk for the relationships to be associated with.
        instance = super(ClientSerializerMixin, self).update(instance, validated_data)
        return instance

    def get_absolute_url(self, obj):
        """
        This function is used ro return absolute url for object
        @param obj: the custom object
        @return: url
        """
        return reverse('client:api:client-detail', kwargs={'pk': obj.pk})
