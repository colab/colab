
from ..utils.apps import ColabProxiedAppConfig
from colab.signals.tasks import register_signal, connect_signal
from colab.plugins.gitlab.tasks import handling_method


class ProxyGitlabAppConfig(ColabProxiedAppConfig):
    name = 'colab.plugins.gitlab'
    verbose_name = 'Gitlab Plugin'
    short_name = 'gitlab'

    signals_list = ['gitlab_create_project']

    def __init__(self, app_name, app_module):
        super(ProxyGitlabAppConfig, self).__init__(app_name, app_module)
        register_signal(self.short_name, self.signals_list)
        connect_signal(self.signals_list[0], self.short_name, handling_method)
