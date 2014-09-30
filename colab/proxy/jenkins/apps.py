
from ..utils.apps import ColabProxiedAppConfig


class ProxyJenkinsAppConfig(ColabProxiedAppConfig):
    name = 'proxy.jenkins'
    verbose_name = 'Jenkins Proxy'
