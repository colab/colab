
from ..utils.apps import ColabProxiedAppConfig


class ProxyJenkinsAppConfig(ColabProxiedAppConfig):
    name = 'jenkins'
    verbose_name = 'Jenkins Proxy'
