from django.apps import AppConfig


class SupervisorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.supervisor'

    def ready(self):
        import apps.supervisor.receivers
