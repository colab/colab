
import abc

class ProxyDataAPI(object):

    @abc.abstractmethod
    def fetch_data(self):
        raise NotImplementedError('fetchData not yet implemented')
