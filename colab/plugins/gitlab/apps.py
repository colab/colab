
from ..utils.apps import ColabPluginAppConfig
from colab.plugins.gitlab.tasks import handling_method
from colab.signals.signals import register_signal, connect_signal


class ProxyGitlabAppConfig(ColabPluginAppConfig):
    name = 'colab.plugins.gitlab'
    verbose_name = 'Gitlab Plugin'
    short_name = 'gitlab'

    signals_list = ['gitlab_create_project']

    def register_signal(self):
        register_signal(self.short_name, self.signals_list)

    def connect_signal(self):
        connect_signal(self.signals_list[0], self.short_name, handling_method)
