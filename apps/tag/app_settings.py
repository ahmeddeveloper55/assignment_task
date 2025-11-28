from ..core.app_settings import AppSettings


class AppSettings(AppSettings):
    """
    This class is used to return values from the project's settings file.
    If this value does not exist, a default value is assigned.
    """


app_settings = AppSettings()
