from django.apps import AppConfig


class OwnerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.editor'

    def ready(self):
        import apps.editor.receivers
