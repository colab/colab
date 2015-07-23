from django.dispatch import Signal
import colab.signals.celery

class Signals():
    def __init__(self):
        self.registered_signals = {}
        self.signal_instances = {}


    def register_signal(self, plugin_name, list_signals):
        for signal in list_signals:
            if signal in self.registered_signals:
                if not plugin_name in self.registered_signals[signal]:
                    self.registered_signals[signal].append(plugin_name)
            else:
                self.registered_signals[signal] = []
                self.registered_signals[signal].append(plugin_name)
                self.signal_instances[signal] = Signal()


    def connect_signal(self, signal_name, sender, handling_method):
        if signal_name in self.signal_instances:
            self.signal_instances[signal_name].connect(handling_method,
                    sender=sender)
        else:
            raise Exception("Signal does not exist!")


    def send(self, signal_name, sender, **kwargs):
        if signal_name in self.signal_instances:
            self.signal_instances[signal_name].send(sender=sender)
        else:
            raise Exception("Signal does not exist!")
