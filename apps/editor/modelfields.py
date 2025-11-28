from django.db import models
from ..core import _
from . import models as editor_models


class IsManagerField(models.BooleanField):
    """
    This field represents the field for the is manger,
    as it can be used in all models built through Django framework.
    """
    description = _("is manger")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("default", False)
        super(IsManagerField, self).__init__(*args, **kwargs)




class EditorField(models.ForeignKey):
    """
    This field represents the field for the editor field,
    as it can be used in all models built through Django framework.
    """
    description = _("editor")

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("to", editor_models.Editor)
        kwargs.setdefault("on_delete", models.CASCADE)
        kwargs.setdefault("related_name", "editorusers")
        super(EditorField, self).__init__(*args, **kwargs)
