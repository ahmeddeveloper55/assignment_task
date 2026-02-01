from django.db import models
from ..core import _
from . import models as editor_models
from ..user import modelfields as user_modelfields



class UserField(user_modelfields.UserOneToOneField):
    """
    This field represents user field,
    as it can be used in all models built through Django framework.
    """

    def __init__(self, *args, **kwargs):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        kwargs.setdefault("default", None)
        kwargs.setdefault("null", True)
        super(UserField, self).__init__(*args, **kwargs)



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
        kwargs.setdefault("related_name", '%(class)s'.lower())
        super(EditorField, self).__init__(*args, **kwargs)
