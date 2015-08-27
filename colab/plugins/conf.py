
from django.conf import settings


def get_plugin_config(app_label):
    return settings.COLAB_APPS.get(app_label, {})
