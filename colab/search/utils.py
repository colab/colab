import importlib
import inspect

from collections import OrderedDict

from django.core.cache import cache
from django.utils.translation import ugettext as _
from django.conf import settings
from colab.super_archives.models import Thread
from colab.proxy.utils.models import CollaborationModel


def get_collaboration_data(filter_by_user=None):
    latest_results = []
    count_types = cache.get('home_chart')
    populate_count_types = False

    if count_types is None:
        populate_count_types = True
        count_types = OrderedDict()
        count_types[_('Emails')] = Thread.objects.count()

    app_names = settings.PROXIED_APPS.keys()

    for app_name in app_names:
        module = importlib
        module = \
            module.import_module('colab.proxy.{}.models'.format(app_name))

        for module_item_name in dir(module):
            module_item = getattr(module, module_item_name)
            if not inspect.isclass(module_item):
                continue
            if not issubclass(module_item, CollaborationModel):
                continue
            if module_item == CollaborationModel:
                continue

            elements = module_item.objects

            if filter_by_user:
                elements = elements.filter(
                    user__username=filter_by_user)
            else:
                elements = elements.all()

            latest_results.extend(elements)

            if populate_count_types:
                count_types[module_item().verbose_name] = elements.count()

    if populate_count_types:
        cache.set('home_chart', count_types, 30)

    return latest_results, count_types
