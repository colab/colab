
from django.apps import AppConfig


class SuperArchivesConfig(AppConfig):
    name = 'super_archives'
    verbose_name = 'Super Archives'

    def ready(self):
        from . import signals
