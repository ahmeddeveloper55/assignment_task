from ..core import _, models as core_models
from ..user import modelfields as user_modelfields
from . import managers, modelfields


class Client(core_models.CommonModel, core_models.TrackedModel):
    """
    This class is used to represent the client's data within the system,
    where each client is represented by the user.
    """
    user = user_modelfields.UserOneToOneField()


    objects = managers.BaseClientManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    def __str__(self):
        """
        This method used to return string of object.
        @return: str
        """
        return f'{self.user.name}'
