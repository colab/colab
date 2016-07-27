import importlib
import inspect

from collections import OrderedDict

from django.core.cache import cache
from django.conf import settings

from colab.plugins.utils.models import Collaboration


def get_collaboration_data(logged_user, filter_by_user=None):
    username = getattr(filter_by_user, 'username', '')
    cache_key = 'home_chart-{}'.format(username)
    count_types = cache.get(cache_key)

    latest_results = []
    populate_count_types = False

    if count_types is None:
        populate_count_types = True
        count_types = OrderedDict()

    for app in settings.COLAB_APPS.values():
        module = importlib.import_module('{}.models'.format(app.get('name')))

        for module_item_name in dir(module):
            module_item = getattr(module, module_item_name)
            if not inspect.isclass(module_item):
                continue
            if not issubclass(module_item, Collaboration):
                continue
            if module_item == Collaboration:
                continue

            queryset = module_item.objects

            if filter_by_user:
                elements = queryset.filter(
                    user__username=filter_by_user)
            else:
                elements = queryset.all()

            latest_results.extend(elements)
            elements_count = elements.count()

            if elements_count > 1:
                verbose_name = module_item._meta.verbose_name_plural.title()
            else:
                verbose_name = module_item._meta.verbose_name.title()

            if populate_count_types:
                count_types[verbose_name] = elements_count

    if populate_count_types:
        cache.set(cache_key, count_types, 30)

    return latest_results, count_types
