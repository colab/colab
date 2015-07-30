import importlib
import inspect

from django.apps import AppConfig
from colab.plugins.utils.signals import AbstractSignal


class ColabProxiedAppConfig(AppConfig):
    colab_proxied_app = True

    def __init__(self, app_name, app_module):
        super(ColabProxiedAppConfig, self).__init__(app_name, app_module)
        self.__import_signals(app_name)
        self.signals.register_signal()


    def _import_signals(self, app_name):
        self.module_path = app_name + '.signals'
        self.module = importlib.import_module(self.module_path)

        for module_item_name in dir(self.module):
            module_item = getattr(self.module, module_item_name)
            if not inspect.isclass(module_item):
                continue
            if issubclass(module_item, AbstractSignal):
                if module_item != AbstractSignal:
                    self.signals = module_item()
                    break


    def ready(self):
        self.signals.connect_signal()
