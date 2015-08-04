
from abc import abstractmethod


class AbstractSignal():

    @abstractmethod
    def register_signal(self):
        raise NotImplementedError

    @abstractmethod
    def connect_signal(self):
        raise NotImplementedError
