from django.apps import AppConfig


class EpisodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.episode'
    verbose_name = 'Episodes'

    def ready(self):
        import apps.episode.receivers
