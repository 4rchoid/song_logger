from django.apps import AppConfig


class SongsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'songs'

    def ready(self):
        from startup import setup_graceful_shutdown
        setup_graceful_shutdown()