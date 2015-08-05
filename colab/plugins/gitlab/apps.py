
from ..utils.apps import ColabProxiedAppConfig


class ProxyGitlabAppConfig(ColabProxiedAppConfig):
    name = 'colab.plugins.gitlab'
    verbose_name = 'Gitlab Plugin'
