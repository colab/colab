
from django.apps import AppConfig


class ColabPluginAppConfig(AppConfig):
    colab_proxied_app = True

    def register_signals(self):
        pass

    def connect_signals(self):
        pass
