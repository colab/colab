from django.conf import settings
import re


def colab_apps(request):
    colab_apps = {}

    for app_name, app in settings.COLAB_APPS.items():
        colab_apps[app_name] = app

    return {'plugins': colab_apps}


def get_prefixes():
    prefixes = []
    for plugin_name in settings.COLAB_APPS:
        plugin = settings.COLAB_APPS[plugin_name]
        prefix = plugin['urls']['prefix']
        change_header = plugin.get('change_header', False)
        if change_header:
            prefixes.append(prefix)
    return prefixes


def change_header(request):
    for prefix in get_prefixes():
        if re.match(prefix, request.path[1:]):
            return {'change_header': True}
    return {'change_header': False}
