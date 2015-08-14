
from django.apps import AppConfig

from .data import register_tasks
from .utils.signals import connect_signal, register_signal


class PluginAppConfig(AppConfig):
    name = 'colab.plugins'

    def ready(self):
        register_signal()
        connect_signal()

        register_tasks()
