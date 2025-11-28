from django.db import models
from ..core import _, modelfields as core_modelfields
from . import models as client_models






class ClientField(models.ForeignKey):
    """
    A client ForeignKey field representing a relationship to the Client model.
    This field can be used in any Django model that requires a link to a Client.
    """

    description = _("client")

    def __init__(self, *args, **kwargs):
        """
        Initializes a new ClientField instance with default values for the
        target model, deletion behavior, and related name, unless explicitly overridden.

        The __init__() method is called automatically when a new object of the class
        is created to set up its attributes.
        """
        kwargs.setdefault("to", client_models.Client)
        kwargs.setdefault("on_delete", models.CASCADE)
        kwargs.setdefault("related_name", '%(class)ss'.lower())
        super(ClientField, self).__init__(*args, **kwargs)
