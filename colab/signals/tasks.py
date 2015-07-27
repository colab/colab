from django.dispatch import Signal
from colab.signals.celery import app


registered_signals = {}
signal_instances = {}


# Fix celery serialization for signal
def reducer(self):
    return (Signal, (self.providing_args,))
Signal.__reduce__ = reducer


def register_signal(plugin_name, list_signals):
    for signal in list_signals:
        if signal in registered_signals:
            if not plugin_name in registered_signals[signal]:
                registered_signals[signal].append(plugin_name)
        else:
            registered_signals[signal] = []
            registered_signals[signal].append(plugin_name)
            signal_instances[signal] = Signal()


def connect_signal(signal_name, sender, handling_method):
    if signal_name in signal_instances:
        signal_instances[signal_name].connect(handling_method.delay,
                sender=sender)
    else:
        raise Exception("Signal does not exist!")


def send(signal_name, sender, **kwargs):
    if signal_name in signal_instances:
        signal_instances[signal_name].send(sender=sender, **kwargs)
    else:
        raise Exception("Signal does not exist!")
