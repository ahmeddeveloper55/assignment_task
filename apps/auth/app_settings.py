from ..core.app_settings import AppSettings
from ..user import RoleChoices


class AppSettings(AppSettings):
    """
    This class is used to return values from the project's settings file.
    If this value does not exist, a default value is assigned.
    """

    @property
    def PHONELESS_CREATION_ROLES(self):
        """
        This name conveys the meaning that the roles specified in this variable are used
        for creating something (e.g. user accounts) when a phone number is not available or does not exist.
        The use of the word "Phoneless" implies the absence of a phone number,
        and "Creation Roles" indicates the roles involved in creating something.
        """
        return self._setting("PHONELESS_CREATION_ROLES", [RoleChoices.CLIENT])

    @property
    def SUPPORTED_METHODS(self):
        """
        Minimum username Length
        """
        return self._setting("SUPPORTED_METHODS", ['sms'])


app_settings = AppSettings()
