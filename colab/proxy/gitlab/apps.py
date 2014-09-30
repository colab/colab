
from ..utils.apps import ColabProxiedAppConfig


class ProxyGitlabAppConfig(ColabProxiedAppConfig):
    name = 'colab.proxy.gitlab'
    verbose_name = 'Gitlab Proxy'
