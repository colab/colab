
from django.dispatch import Signal

from .exceptions import SignalDoesNotExist

registered_signals = {}
signal_instances = {}


class ColabSignal(Signal):
    def __reduce__(self):
        """

        In order to send a signal to a celery task, it is necessary to pickle
        the objects that will be used as parameters. However,
        django.dispatch.Signal has an instance of threading.Lock, which is an
        object that cannot be pickled. Therefore, this function changes the
        pickle behaviour of Signal, making that only the providind_args of
        Signal to be pickled."""

        return (ColabSignal, (self.providing_args,))


def register_signal(plugin_name, list_signals):
    for signal in list_signals:
        if signal in registered_signals:
            if plugin_name not in registered_signals[signal]:
                registered_signals[signal].append(plugin_name)
        else:
            registered_signals[signal] = []
            registered_signals[signal].append(plugin_name)
            signal_instances[signal] = ColabSignal()


def connect_signal(signal_name, sender, handling_method):
    if signal_name in signal_instances:
        signal_instances[signal_name].connect(handling_method.delay,
                                              sender=sender)
    else:
        raise SignalDoesNotExist


def send(signal_name, sender, **kwargs):
    if signal_name in signal_instances:
        signal_instances[signal_name].send(sender=sender, **kwargs)
    else:
        raise SignalDoesNotExist
