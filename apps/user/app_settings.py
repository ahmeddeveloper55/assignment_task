from ..core.app_settings import AppSettings


class AppSettings(AppSettings):
    """
    This class is used to return values from the project's settings file.
    If this value does not exist, a default value is assigned.
    """

    @property
    def DEFAULT_USER_IMAGE(self):
        """
        Return the default image to the user if there is no image.
        """
        return self._setting("DEFAULT_USER_IMAGE", None)


app_settings = AppSettings()
