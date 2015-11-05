
from django.apps import AppConfig
from ..conf import get_plugin_config


class ColabPluginAppConfig(AppConfig):
    colab_proxied_app = True
    namespace = None

    def __init__(self, app_name, app_module):
        super(ColabPluginAppConfig, self).__init__(app_name, app_module)
        self.set_namespace()

    def set_namespace(self):
        config = get_plugin_config(self.name)
        config['urls']['namespace'] = self.namespace

    def register_signal(self):
        pass

    def connect_signal(self):
        pass
