
from ..utils.apps import ColabProxiedAppConfig


class ProxyJenkinsAppConfig(ColabProxiedAppConfig):
    name = 'colab.proxy.jenkins'
    verbose_name = 'Jenkins Proxy'
