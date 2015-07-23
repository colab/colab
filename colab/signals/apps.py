
from django.apps import AppConfig


class SignalsConfig(AppConfig):
    name = 'colab.signals'
    registered_signals = {}
    signal_instances = {}
