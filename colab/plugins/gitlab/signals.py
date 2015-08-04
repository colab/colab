from colab.plugins.utils.signals import AbstractSignal
from colab.plugins.gitlab.tasks import handling_method
from colab.signals.signals import register_signal, connect_signal


class GitlabSignals(AbstractSignal):

    short_name = 'gitlab'
    signals_list = ['gitlab_create_project']

    def register_signal(self):
        register_signal(self.short_name, self.signals_list)

    def connect_signal(self):
        connect_signal(self.signals_list[0], self.short_name, handling_method)
