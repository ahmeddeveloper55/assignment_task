import pytz

from .utils.translation import _

default_app_config = 'apps.core.apps.CoreConfig'


def get_timezone_choices():
    """
    This function is used to return timezone choices.
    """

    return [(n, n) for n in pytz.all_timezones]
