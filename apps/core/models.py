from django.db import models
from django_softdelete.models import SoftDeleteModel as BaseSoftDeleteModel
from .utils import datetime
from . import managers, modelfields


class CoreModel(models.Model):
    """
    This class is an abstract class will be used in all models in this system, as it will contain the default settings,
    which must be present in all other models within the system.
    Such settings define the default manager class and also define some fields that all models will share.
    """
    id = modelfields.UUIDField()

    objects = models.Manager()

    class Meta:
        abstract = True

    def update_fields(self, **kwargs):
        """
        This function is used to update the instance fields, as it will facilitate
        the modification of the instance data without making a new query
        """
        [setattr(self, field, value) for field, value in kwargs.items()]
        return self

    def update(self, **kwargs):
        """
        This function is used to update the instance data, as it will facilitate
        the modification of the instance data without making a new query
        """
        self.update_fields(**kwargs)
        self.save()
        return self


class CommonModel(CoreModel):
    """
    This class is an abstract class contains a set of fields that will be shared by the different models in the system,
    such as the date of creation, the date of modification, and others.
    """
    created_at = modelfields.CreatedAtField()

    updated_at = modelfields.UpdatedAtField()

    class Meta:
        ordering = ['-created_at']
        abstract = True


class ActivateModel(CoreModel):
    """
    This class is an abstract class used to add functionality to active or disable objects within the model.
    """
    is_active = modelfields.IsActiveField()

    enabled_at = modelfields.EnabledAtField()

    activated_objects = managers.ActivatedManager()
    disabled_objects = managers.DisabledManager()

    class Meta:
        abstract = True

    def active(self):
        """
        this function is used to active object.
        """
        self.is_active = True
        self.enabled_at = datetime.now()
        self.save()

    def disable(self):
        """
        this function is used to disable object.
        """
        self.is_active = False
        self.enabled_at = None
        self.save()

    @property
    def is_disabled(self):
        """
        This function returns true if the object is disabled.
        """
        return not self.is_active


class SoftDeleteModel(BaseSoftDeleteModel, CoreModel):
    """
    This is a set of small classes to make soft deletion of objects.
    Use the abstract model SoftDeleteModel for adding two new fields: is_deleted - is a boolean field,
    shows weather of a deletion state of object.
    """
    global_objects = None
    undeleted_objects = managers.UndeletedManager()

    class Meta:
        abstract = True


class VerifiedModel(ActivateModel, SoftDeleteModel):
    """
    This class contains the features of activate and delete model.
    You can use it when you want to inherit all these properties together.
    """
    verified_objects = managers.VerifiedManager()

    class Meta:
        abstract = True


class CreatedAndUpdatedByModel(CoreModel):
    """
    This class is an abstract class used to add created by field to the model.
    """
    created_by = modelfields.CreatedByField()

    updated_by = modelfields.UpdatedByField()

    class Meta:
        abstract = True


class TrackedModel(CoreModel):
    """
    This class is an abstract class used to add created by field to the model.
    """
    created_by = modelfields.CreatedByField()

    updated_by = modelfields.UpdatedByField()

    class Meta:
        abstract = True
