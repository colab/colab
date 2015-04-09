
from django.conf import settings


def colab_apps(request):
    colab_apps = {}

    for app_name, app in settings.COLAB_APPS.items():
        colab_apps[app_name] = app

    return {'plugins': colab_apps}
