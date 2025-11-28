from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..core import _, serializerfields as core_serializerfields
from . import models, permissions, RoleChoices
from ..core.serializerfields import Field

UserModel = get_user_model()


class CurrentUserDefault:
    """
    This class used to return user object form http request
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
            if user is not None and user.is_authenticated:
                return user
        return None

    def __repr__(self):
        """
        special methods are a set of predefined methods used to enrich your classes.
        They start and end with double underscores.
        :return:
        """
        return '%s()' % self.__class__.__name__


class RoleField(core_serializerfields.ChoiceField):
    """
    This field represents the role field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("label", _('role'))
        kwargs.setdefault("required", True)
        kwargs.setdefault("choices", RoleChoices.choices)
        super(RoleField, self).__init__(*args, **kwargs)


class UsernameField(core_serializerfields.CharField):
    """
    This field represents the username field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("label", _('username'))
        kwargs.setdefault("required", True)
        super(UsernameField, self).__init__(**kwargs)


class PasswordField(core_serializerfields.CharField):
    """
    This field represents the password field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("label", _('password'))
        kwargs.setdefault("required", True)
        super(PasswordField, self).__init__(**kwargs)


class ConfirmPasswordField(PasswordField):
    """
    This field represents the confirmation password field,
    as it can be used in all serializers built through Django Restfull framework.
    """

    def __init__(self, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("label", _('confirmation password'))
        kwargs.setdefault("required", True)
        kwargs.setdefault("write_only", True)
        super(PasswordField, self).__init__(**kwargs)


class PhoneNumberField(core_serializerfields.PhoneNumberField):
    """
    This field represents the phone number field,
    as it can be used in all serializers built through Django Restfull framework.
    """
    default_error_messages = {
        'unique': _('A user with that phone number already exists.')
    }

    def __init__(self, role, instance=None, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        self.role = role
        self.instance = instance
        kwargs.setdefault('required', False if instance else True)
        super(PhoneNumberField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        """
        The to_internal_value method is responsible for converting incoming data
        into a Python object during deserialization.
        You can override this method in a custom serializer field to perform custom
        validation or convert the input data into a different Python object.
        """
        data = super(PhoneNumberField, self).to_internal_value(data)
        queryset = UserModel.objects.find_by_phone_number(data, role=self.role)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            self.fail('unique')

        return data


class EmailField(core_serializerfields.EmailField):
    """
    This field represents the email field,
    as it can be used in all serializers built through Django Restfull framework.
    """
    default_error_messages = {
        'unique': _('A user with that email already exists.')
    }

    def __init__(self, role, instance=None, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        self.role = role
        self.instance = instance
        kwargs.setdefault('required', False if instance else True)
        super(EmailField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        """
        The to_internal_value method is responsible for converting incoming data
        into a Python object during deserialization.
        You can override this method in a custom serializer field to perform custom
        validation or convert the input data into a different Python object.
        """
        data = super(EmailField, self).to_internal_value(data)
        queryset = UserModel.objects.find_by_email(data, role=self.role)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            self.fail('unique')

        return data




class UserField(core_serializerfields.PrimaryKeyRelatedField):
    """
    This field represents the field for the user field,
    as it can be used in all serializers built through Django Restfull framework.
    """
    queryset = models.User.objects.none()

    def get_queryset(self):
        return permissions.UserAccessPolicy.scope_queryset(self.request, self.queryset)

    def get_value(self, dictionary):
        # We always use the default value for `HiddenField`.
        # User input is never provided or accepted.
        return getattr(CurrentUserDefault()(self), 'pk', None)
