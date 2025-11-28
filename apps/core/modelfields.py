import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models
from django.core import validators
from django_resized import ResizedImageField as BaseResizedImageField
from phonenumber_field.modelfields import PhoneNumberField as BasePhoneNumberField
from sort_order_field import SortOrderField as BaseSortOrderField

from .utils.uploads import image_folder, file_folder
from . import _, get_timezone_choices


class UUIDField(models.UUIDField):
    """
    This field represents the uuid field,
    as it can be used in all models built through Django framework.
    """
    description = _("id")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("primary_key", True)
        kwargs.setdefault("default", uuid.uuid4)
        kwargs.setdefault("editable", False)
        super(UUIDField, self).__init__(*args, **kwargs)


class ContentTypeField(models.ForeignKey):
    """
    This field represents the content type field,
    as it can be used in all models built through Django framework.
    """
    description = _("content type")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("to", ContentType)
        kwargs.setdefault("on_delete", models.CASCADE)
        super(ContentTypeField, self).__init__(*args, **kwargs)


class ObjectIdField(models.UUIDField):
    """
    This field represents the object id,
    as it can be used in all models built through Django framework.
    """
    description = _("object id")


class ContentObjectField(GenericForeignKey):
    """
    This field represents the content object,
    as it can be used in all models built through Django framework.
    """
    description = _("content object")


class PhoneNumberField(BasePhoneNumberField):
    """
    This field represents the phone number field,
    as it can be used in all models built through Django framework.
    """
    description = _("phone number")

class UrlField(models.URLField):
    """
        This field represents the UrlField field,
        as it can be used in all models built through Django framework.
        """
    def __init__(self, *args, **kwargs):
        # default was 200; increase so real CDN URLs fit
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        kwargs.setdefault("max_length", 1000)
        super().__init__(*args, **kwargs)


class EmailField(models.EmailField):
    """
    This field represents the email field,
    as it can be used in all models built through Django framework.
    """
    description = _("email")

    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(EmailField, self).to_python(value)
        # Value can be None so check that it's a string before lower.
        if isinstance(value, str):
            return value.lower()
        return value


class SlugField(models.SlugField):
    """
    This field represents the slug field,
    as it can be used in all models built through Django framework.
    """
    default_validators = [validators.validate_unicode_slug]
    description = _("slug")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("max_length", 255)
        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("unique", True)
        kwargs.setdefault("editable", False)
        super(SlugField, self).__init__(*args, **kwargs)


class NameField(models.CharField):
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
        kwargs.setdefault("max_length", 255)
        super(NameField, self).__init__(*args, **kwargs)





class TimezoneField(models.CharField):
    """
    This field represents the timezone field,
    as it can be used in all models built through Django framework.
    """
    description = _("timezone")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("max_length", 100)
        kwargs.setdefault("default", 'Asia/Riyadh')
        kwargs.setdefault("choices", get_timezone_choices())
        super(TimezoneField, self).__init__(*args, **kwargs)


class ResizedImageField(BaseResizedImageField):
    """
    This field represents the image field for,
    as it can be used in all models built through Django framework.
    """
    description = _("image")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("quality", 100)
        kwargs.setdefault("null", True)
        kwargs.setdefault("upload_to", image_folder)
        super(ResizedImageField, self).__init__(*args, **kwargs)


class IconField(ResizedImageField):
    """
    This field represents the image field,
    as it can be used in all models built through Django framework.
    """
    description = _("icon")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("null", True)
        super(IconField, self).__init__(*args, **kwargs)


class FileField(models.FileField):
    """
    This field represents the file field,
    as it can be used in all models built through Django framework.
    """
    description = _("file")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("upload_to", file_folder)
        super(FileField, self).__init__(*args, **kwargs)


class SortOrderField(BaseSortOrderField):
    """
    This field represents the sort order field,
    as it can be used in all models built through Django framework.
    """
    description = _("sort order")
    default_validators = [MinValueValidator(0)]


class PositiveIntegerField(models.PositiveIntegerField):
    """
    This field represents the positive integer field,
    as it can be used in all models built through Django framework.
    """
    description = _("positive integer")
    default_validators = [MinValueValidator(0)]


class CreatedByField(models.ForeignKey):
    """
    This field represents the created by field,
    as it can be used in all models built through Django framework.
    """
    description = _("created by")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """

        kwargs.setdefault("to", settings.AUTH_USER_MODEL)
        kwargs.setdefault("on_delete", models.SET_NULL)
        kwargs.setdefault("related_name", '%(class)s_created_by')
        kwargs.setdefault("null", True)
        super(CreatedByField, self).__init__(*args, **kwargs)


class UpdatedByField(CreatedByField):
    """
    This field represents the updated by field,
    as it can be used in all models built through Django framework.
    """
    description = _("updated by")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("related_name", '%(class)s_updated_by')
        super(UpdatedByField, self).__init__(*args, **kwargs)


class CreatedAtField(models.DateTimeField):
    """
    This field represents the created at field,
    as it can be used in all models built through Django framework.
    """
    description = _("created at")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("auto_now_add", True)
        kwargs.setdefault("editable", False)
        super(CreatedAtField, self).__init__(*args, **kwargs)


class UpdatedAtField(models.DateTimeField):
    """
    This field represents the updated at field,
    as it can be used in all models built through Django framework.
    """
    description = _("updated at")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("auto_now", True)
        kwargs.setdefault("editable", False)
        super(UpdatedAtField, self).__init__(*args, **kwargs)


class IsActiveField(models.BooleanField):
    """
    This field represents the is active,
    as it can be used in all models built through Django framework.
    """
    description = _("is active")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("default", True)
        super(IsActiveField, self).__init__(*args, **kwargs)


class EnabledAtField(models.DateTimeField):
    """
    This field represents the enabled at field,
    as it can be used in all models built through Django framework.
    """
    description = _("enabled at")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("editable", False)
        kwargs.setdefault("null", True)
        super(EnabledAtField, self).__init__(*args, **kwargs)


class DescriptionField(models.TextField):
    """
    This field represents the description field,
    as it can be used in all models built through Django framework.
    """
    description = _("description")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        super(DescriptionField, self).__init__(*args, **kwargs)


class NoteField(models.TextField):
    """
    This field represents the note field,
    as it can be used in all models built through Django framework.
    """
    description = _("note")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("blank", True)
        kwargs.setdefault("null", True)
        super(NoteField, self).__init__(*args, **kwargs)
