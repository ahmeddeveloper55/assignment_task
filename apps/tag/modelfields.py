from django.db import models

from ..core import _
from . import models as tag_models


class TagField(models.ForeignKey):
    """
    This field represents the tag field,
    as it can be used in all models built through Django framework.
    """

    description = _("tag")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("to", tag_models.Tag)
        kwargs.setdefault("on_delete", models.CASCADE)
        kwargs.setdefault("related_name", '(class)ss'.lower())
        super(TagField, self).__init__(*args, **kwargs)


class TagsField(models.ManyToManyField):
    """
    This field represents the tag field,
    as it can be used in all models built through Django framework.
    """

    description = _("tags")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("to", tag_models.Tag)
        kwargs.setdefault("related_name", '%(class)ss'.lower())
        super(TagsField, self).__init__(*args, **kwargs)
