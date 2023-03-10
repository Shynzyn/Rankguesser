from django.apps import AppConfig


class QuesserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guesser'


class GuesserConfig(AppConfig):
    name = 'guesser'

    def ready(self):
        from .signals import create_profile, save_profile
