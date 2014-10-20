
from django.apps import apps


def proxied_apps(request):
    proxied_apps = {}

    for app in apps.get_app_configs():
        if getattr(app, 'colab_proxied_app', False):
            proxied_apps[app.label] = True

    return {'proxy': proxied_apps}
