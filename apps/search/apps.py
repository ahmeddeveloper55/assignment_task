from django.apps import AppConfig


class ProgramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.search'
    verbose_name = 'searches'

    def ready(self):
        import apps.program.receivers
