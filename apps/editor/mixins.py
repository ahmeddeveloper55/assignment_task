from django.urls import reverse
from rest_framework import serializers
from rest_access_policy import FieldAccessMixin
from ..core import permissions, serializers as core_serializers, serializerfields as core_serializerfields
from . import models, serializerfields
from ..user import mixins as user_mixins
from ..user import serializerfields as user_serializerfields

class EditorSerializerMixin(user_mixins.UserSerializerMixin):
    """
    This class can handle the add and modify functions of the editor model and
    return all the objects associated with this table.
    This class represents an abstract class that you can use in any app you want
    and modify the functions through inheritance operations
    """
    absolute_url = core_serializerfields.AbsoluteUrlField()
    role = serializerfields.RoleField()
    name_en = serializers.CharField(source='editor.name_en', required=False, allow_blank=True)
    name_ar = serializers.CharField(source='editor.name_ar', required=False, allow_blank=True)
    description = serializers.CharField(source='editor.description', required=False, allow_blank=True, allow_null=True)
    confirm = user_serializerfields.ConfirmPasswordField(required=False, write_only=True)


    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        super(EditorSerializerMixin, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        representation = super(EditorSerializerMixin, self).to_representation(instance)
        representation.pop('password', None)
        representation.pop('confirm', None)
        return representation

    def get_extra_kwargs(self):
        """
        Make password required only on create (like Member).
        """
        extra_kwargs = super().get_extra_kwargs()
        if self.instance:
            extra_kwargs['password'] = {'required': False}
        else:
            extra_kwargs['password'] = {'required': True}
        return extra_kwargs

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:

        return ExampleModel.objects.create(**validated_data)
        """
        editor_data = validated_data.pop('editor', {})
        validated_data.pop('confirm', None)

        user = super(EditorSerializerMixin, self).create(validated_data)

        if not editor_data.get('name'):
            editor_data['name'] = editor_data.get('name_en') or editor_data.get('name_ar') or user.name or user.username
        editor_data.setdefault('email', user.email)
        editor_data.setdefault('phone_number', user.phone_number)

        models.Editor.objects.create(user=user, **editor_data)
        return user

    def update(self, instance, validated_data):
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates, we already
        # have an instance pk for the relationships to be associated with.
        editor_data = validated_data.pop('editor', None)
        validated_data.pop('confirm', None)

        user = super(EditorSerializerMixin, self).update(instance, validated_data)

        if editor_data is not None:
            editor, _ = models.Editor.objects.get_or_create(user=user)
            if not editor_data.get('name') and not editor.name:
                editor_data['name'] = editor_data.get('name_en') or editor_data.get('name_ar') or user.name or user.username
            if editor.email in (None, ''):
                editor_data.setdefault('email', user.email)
            if editor.phone_number in (None, ''):
                editor_data.setdefault('phone_number', user.phone_number)

            for key, value in editor_data.items():
                setattr(editor, key, value)
            editor.save()

        return user

    def get_absolute_url(self, obj):
        """
        This function is used ro return absolute url for object
        @param obj: the custom object
        @return: url
        """
        return reverse('editor:api:editor-detail', kwargs={'pk': obj.pk})
