
import abc

from django.conf import settings


class PluginDataImporter(object):

    def __init__(self):
        self.config = settings.COLAB_APPS.get(self.app_label, {})

    @abc.abstractmethod
    def fetch_data(self):
        raise NotImplementedError
    fetch_data.is_abstract = True

    @abc.abstractmethod
    def app_label(self):
        raise NotImplementedError
