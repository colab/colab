
from abc import abstractmethod


class AbstractSignal(object):

    @abstractmethod
    def register_signal(self):
        raise NotImplementedError

    @abstractmethod
    def connect_signal(self):
        raise NotImplementedError
