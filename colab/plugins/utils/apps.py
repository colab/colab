
from django.apps import AppConfig


class ColabPluginAppConfig(AppConfig):
    colab_proxied_app = True

    def register_signal(self):
        pass

    def connect_signal(self):
        pass
