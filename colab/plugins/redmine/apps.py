
from ..utils.apps import ColabProxiedAppConfig


class ProxyRedmineAppConfig(ColabProxiedAppConfig):
    name = 'colab.plugins.redmine'
    verbose_name = 'Redmine Proxy'
