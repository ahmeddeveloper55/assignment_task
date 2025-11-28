from ...core import utils
from ..app_settings import app_settings


def get_image_url(image):
    """
    This function is used to return the full link of the image associated with the user.
    @return: The url of Image.
    """
    return image.url if image else app_settings.DEFAULT_USER_IMAGE


def get_age(birthdate):
    """
    This function is used to return the calculate the age from birthdate.
    @return: age.
    """
    if birthdate is None:
        return 0

    today = utils.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age
