from .app_settings import app_settings

default_app_config = 'apps.auth.apps.AuthConfig'


def get_methods_choices():
    """
    This function is used to return methods choices like sms or call.
    """

    from two_factor.plugins.registry import registry
    return [(m.code, m.verbose_name) for m in registry.get_methods() if m.code in app_settings.SUPPORTED_METHODS]
