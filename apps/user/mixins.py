from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import serializers
from rest_access_policy import FieldAccessMixin
from ..core import permissions, serializers as core_serializers, serializerfields as core_serializerfields
from . import models, serializerfields
from django.templatetags.static import static

# Retrieve the user model set in the current Django project
UserModel = get_user_model()


class ProfileSerializerMixin(core_serializers.ModelSerializer):
    """
    This class can handle the add and modify functions of the profile model and
    return all the objects associated with this table.
    This class represents an abstract class that you can use in any app you want
    and modify the functions through inheritance operations
    """

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        self.fields.update({
            'gender_display': serializers.CharField(source='get_gender_display',read_only=True)
        })
        return super(ProfileSerializerMixin, self).to_representation(instance)

    class Meta:
        abstract = True
        model = models.Profile
        exclude = ('id', 'user', 'created_at', 'updated_at')


class UserSerializerMixin(FieldAccessMixin, core_serializers.ModelSerializer):
    """
    This class can handle the add and modify functions of the user model and
    return all the objects associated with this table.
    This class represents an abstract class that you can use in any app you want
    and modify the functions through inheritance operations
    """
    profile = ProfileSerializerMixin(required=False)


    absolute_url = core_serializerfields.AbsoluteUrlField()

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        super(UserSerializerMixin, self).__init__(*args, **kwargs)
        if not self.is_post_action():
            self.fields['role'].read_only = True

        role = self.get_field_value('role')
        self.fields['phone_number'] = serializerfields.PhoneNumberField(role, instance=self.instance)
        self.fields['email'] = serializerfields.EmailField(role, instance=self.instance)

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        self.fields.update({
            'role_display': serializers.CharField(source='get_role_display', read_only=True),
            'login_allowed': serializers.BooleanField(source='is_login_allowed', read_only=True),
            'request_deletion': serializers.BooleanField(source='is_request_deletion',read_only=True),
        })
        return super(UserSerializerMixin, self).to_representation(instance)

    class Meta:
        abstract = True
        model = UserModel
        access_policy = permissions.SafeAccountAccessPolicy
        exclude = ('user_permissions', 'groups', 'is_superuser', 'is_staff', 'is_deleted')
        read_only_fields = ('is_active', 'enabled_at', 'last_login', 'created_at', 'updated_at')
        extra_kwargs = {'username': {'required': False}, 'password': {'required': False}}

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:

        return ExampleModel.objects.create(**validated_data)
        """
        profile = validated_data.pop('profile', None)
        instance = self.Meta.model.objects.create_user(**validated_data)

        if profile is not None:
            self.fields["profile"].update(instance.profile, profile)

        return instance

    def update(self, instance, validated_data):
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates, we already
        # have an instance pk for the relationships to be associated with.
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)

        if profile_data:
            self.fields["profile"].update(instance.profile, profile_data)

        if password is not None:
            instance.set_password(password)

        return super(UserSerializerMixin, self).update(instance, validated_data)


   
    def get_absolute_url(self, obj):
        """
        This function is used ro return absolute url for object
        @param obj: the custom object
        @return: url
        """
        return reverse('user:api:user-detail', kwargs={'pk': obj.pk})
