from ..core import _, serializerfields as core_serializerfields
from ..user import serializerfields as user_serializerfields, RoleChoices
from . import models, permissions


class CurrentEditorDefault:
    """
    This class used to return eidtor object form http request
    """

    requires_context = True

    def __call__(self, serializer_field):
        """
        method enables Python programmers to write classes where the instances
        behave like functions and can be called like a function.
        :return: user object
        """
        request = serializer_field.context.get('request', None)
        if request is not None:
            user = getattr(request, 'user', None)
            if user is not None and user.is_editor:
                return user.editoruser.editor
        return None

    def __repr__(self):
        """
        special methods are a set of predefined methods used to enrich your classes.
        They start and end with double underscores.
        :return:
        """
        return '%s()' % self.__class__.__name__


class PhoneNumberField(user_serializerfields.PhoneNumberField):
    """
    This field represents the field for the phone number,
    as it can be used in all serializers built through Django Restfull framework.
    """

    default_error_messages = {
        'unique': _('An Editor with that phone number already exists.')
    }

    def __init__(self, instance=None, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault('role', RoleChoices.EDITOR)
        kwargs.setdefault('instance', self.get_user_instance(instance))
        super(PhoneNumberField, self).__init__(**kwargs)

    def get_user_instance(self, editor):
        """
        This method is used to return the user instance from owner.
        @return: user.
        """
        if not isinstance(editor, models.Editor):
            return None

        return editor.manager()



class EditorField(core_serializerfields.PrimaryKeyRelatedField):
    """
    This field represents the field for the owner field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    queryset = models.Editor.objects.none()

    def get_queryset(self):
        return permissions.EditorAccessPolicy.scope_queryset(self.request, self.queryset)

    def get_value(self, dictionary):
        # We always use the default value for `HiddenField`.
        # User input is never provided or accepted.

        if self.user.is_owner:
            return getattr(CurrentEditorDefault()(self), 'pk', None)

        return super(EditorField, self).get_value(dictionary)


class RoleField(core_serializerfields.HiddenField):
    """
    This field represents the field for the role field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault('default', RoleChoices.ADMIN)
        super().__init__(**kwargs)