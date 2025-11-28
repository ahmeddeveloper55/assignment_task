from django.conf import settings
from .utils import model


class AppSettings(object):
    """
    This class is used to return values from the project's settings file.
    If this value does not exist, a default value is assigned.
    """

    def _setting(self, name, default):
        getter = getattr(
            settings,
            "CORE_SETTING_GETTER",
            lambda name, default: getattr(settings, name, default),
        )

        return getter(name, default)

    def _get_model(self, res):
        """
        This function is used to get model from res value.
        """

        app_label, model_name = res.split('.', maxsplit=1)
        return model.get_model(app_label, model_name)

    def DEFAULT_TIMEZONE(self):
        """
        This function is used to return the default timezone.
        Returns: default timezone
        """
        return self._setting("DEFAULT_TIMEZONE", 'Asia/Riyadh')


app_settings = AppSettings()
