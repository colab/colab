
import abc

from django.conf import settings


class ProxyDataAPI(object):

    def __init__(self):
        self.config = settings.COLAB_APPS.get(self.app_label, {})

    @abc.abstractmethod
    def fetch_data(self):
        raise NotImplementedError('fetchData not yet implemented')
