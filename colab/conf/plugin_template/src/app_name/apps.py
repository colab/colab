
from colab.plugins.utils.apps import ColabPluginAppConfig


class {{ app_name_camel }}AppConfig(ColabPluginAppConfig):
    name = '{{ app_name }}'
    verbose_name = '{{ app_name_verbose }} Plugin'
    short_name = '{{ app_name }}'
