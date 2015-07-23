from django.dispatch import Signal
from colab.signals.celery import app

registered_signals = {}
signal_instances = {}


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
        signal_instances[signal_name].connect(handling_method,
                sender=sender)
    else:
        raise Exception("Signal does not exist!")


@app.task(bind=True)
def send(self, signal_name, sender, **kwargs):
    if signal_name in signal_instances:
        signal_instances[signal_name].send(sender=sender)
    else:
        raise Exception("Signal does not exist!")
