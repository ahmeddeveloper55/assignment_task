import logging
from django.core import exceptions

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_content_type_by_model_name(model_name):
    """
    This function is used to get the content type model using name of model.
    returnL content type.
    """
    from django.contrib.contenttypes import models

    try:
        content_type = models.ContentType.objects.get(model=model_name)
        return content_type
    except exceptions.ObjectDoesNotExist:
        raise ValueError(f"Model with name '{model_name}' does not exist.")


def get_object_by_model_class(model_class, object_id):
    """
    This function is used to get the object from model_class.
    returnL object.
    """
    try:
        return model_class.objects.get(pk=object_id)
    except exceptions.ObjectDoesNotExist:
        raise ValueError(f"The object {object_id} is non-existent.")
