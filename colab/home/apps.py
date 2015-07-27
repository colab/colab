
from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'colab.home'

    def ready(self):
        from ..celery import app  # noqa
