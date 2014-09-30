
from ..utils.apps import ColabProxiedAppConfig


class ProxyGitlabAppConfig(ColabProxiedAppConfig):
    name = 'proxy.gitlab'
    verbose_name = 'Gitlab Proxy'
