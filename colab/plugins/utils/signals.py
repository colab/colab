
from django.apps import apps


def _init_signals(method_name):
    for app in apps.get_app_configs():
        # Try to get the method with `method_name`.
        #   If it exists call it using `app` as the first parameter.
        #   This is required because methods take `self` as first
        #   parameter and as we are calling it as a function python
        #   won't send it explicitly.
        # If the method doesn't exist we return a dummy function that
        #   won't do anything.
        getattr(app, method_name, lambda: None)()


def register_signal():
    _init_signals('register_signal')


def connect_signal():
    _init_signals('connect_signal')
