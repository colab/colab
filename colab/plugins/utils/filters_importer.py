#!/usr/bin/env python

import importlib

from django.conf import settings


def import_plugin_filters(request):
    plugin_filters = {}
    for app_name in settings.INSTALLED_APPS:

        module_name = '{}.filters'.format(app_name)
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue

        get_filters = getattr(module, 'get_filters', None)
        if get_filters:
            plugin_filters.update(get_filters(request))

    return plugin_filters
