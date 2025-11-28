from django.apps import AppConfig


class TagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tag'

    def ready(self):
        import apps.tag.receivers
