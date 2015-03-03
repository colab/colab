
from django.apps import apps
from django.conf import settings


def proxied_apps(request):
    proxied_apps = {}

    for app_name, app in settings.COLAB_APPS.items():
        proxied_apps[app_name] = app

    return {'proxy': proxied_apps}
