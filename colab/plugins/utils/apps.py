
from django.apps import AppConfig


class ColabProxiedAppConfig(AppConfig):
    colab_proxied_app = True

    def register_signals(self):
        pass

    def connect_signals(self):
        pass
