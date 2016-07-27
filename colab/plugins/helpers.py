from colab.plugins.exceptions import PluginDoesNotExistError
from django.utils.translation import ugettext as _
from django.conf import settings


def get_plugin_config(plugin_name):
    try:
        return settings.COLAB_APPS[plugin_name]
    except KeyError:
        raise PluginDoesNotExistError(
            _("Plugin {} does not exist.".format(plugin_name))
        )


def get_plugin_prefix(plugin_name, regex=True):
    config = get_plugin_config(plugin_name)
    urls = config.get("urls")
    prefix = urls.get("prefix")

    if not regex:
        prefix = prefix.replace("^", "")
    return prefix
