from django.db import models
from django.conf import settings
from ..core import _, modelfields as core_modelfields
from . import validators, RoleChoices, GenderChoices


class NameField(core_modelfields.NameField):
    """
    This field represents the name field,
    as it can be used in all models built through Django framework.
    """

    description = _("name")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """

        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)
        super(NameField, self).__init__(*args, **kwargs)


class PhoneNumberField(core_modelfields.PhoneNumberField):
    """
    This field represents the phone number field,
    as it can be used in all models built through Django framework.
    """


class UsernameField(models.CharField):
    """
    This field represents the username field,
    as it can be used in all models built through Django framework.
    """

    default_validators = [validators.validate_username]
    description = _("username")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """

        kwargs.setdefault("max_length", 150)
        kwargs.setdefault("unique", True)
        super(UsernameField, self).__init__(*args, **kwargs)


class EmailField(core_modelfields.EmailField):
    """
    This field represents the email field,
    as it can be used in all models built through Django framework.
    """

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """

        kwargs.setdefault("null", True)
        super(EmailField, self).__init__(*args, **kwargs)


class RoleField(models.CharField):
    """
    This field represents the role field for,
    as it can be used in all models built through Django framework.
    """

    description = _("role")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """

        kwargs.setdefault("max_length", 100)
        kwargs.setdefault("choices", RoleChoices.choices)
        super(RoleField, self).__init__(*args, **kwargs)


class GenderField(models.CharField):
    """
    This field represents the gender field,
    as it can be used in all models built through Django framework.
    """

    description = _("gender")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """

        kwargs.setdefault("max_length", 20)
        kwargs.setdefault("null", True)
        kwargs.setdefault("choices", GenderChoices.choices)
        super(GenderField, self).__init__(*args, **kwargs)




class UserOneToOneField(models.OneToOneField):
    """
    This field represents user field,
    as it can be used in all models built through Django framework.
    """

    description = _("user")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """

        kwargs.setdefault("to", settings.AUTH_USER_MODEL)
        kwargs.setdefault("on_delete", models.CASCADE, )
        kwargs.setdefault("related_name", '%(class)s'.lower())
        super(UserOneToOneField, self).__init__(*args, **kwargs)


class UserField(models.ForeignKey):
    """
    This field represents the users field,
    as it can be used in all models built through Django framework.
    """

    description = _("user")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """

        kwargs.setdefault("to", settings.AUTH_USER_MODEL)
        kwargs.setdefault("on_delete", models.CASCADE, )
        kwargs.setdefault("related_name", '%(class)ss'.lower())
        super(UserField, self).__init__(*args, **kwargs)


class UsersField(models.ManyToManyField):
    """
    This field represents the field for the users field,
    as it can be used in all models built through Django framework.
    """

    description = _("users")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("to", 'user.user')
        kwargs.setdefault("related_name", '%(class)ss'.lower())
        super(UsersField, self).__init__(*args, **kwargs)


