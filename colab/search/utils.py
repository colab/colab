import importlib
import inspect

from collections import OrderedDict

from django.core.cache import cache
from django.utils.translation import ugettext as _
from django.apps import apps
from django.conf import settings
from colab.super_archives.models import Thread
from colab.search.preview_block import PreviewBlock


def trans(key):
    translations = {
        'wiki': _('Wiki'),
        'thread': _('Emails'),
        'changeset': _('Code'),
        'ticket': _('Tickets'),
        'attachment': _('Attachments'),
    }

    app_names = settings.PROXIED_APPS.keys()

    for app_name in app_names:
        collaboration_models = \
            apps.get_app_config(app_name).collaboration_models

        for collaboration in collaboration_models:
            translations[collaboration['model'].lower()] = \
                collaboration['model_verbose']

    return translations.get(key, key)


def getCollaborationData(filter_by_user=None):

    latest_results = []
    count_types = cache.get('home_chart')
    populate_count_types = False

    if count_types is None:
        populate_count_types = True
        count_types = OrderedDict()
        count_types['thread'] = Thread.objects.count()

    app_names = settings.PROXIED_APPS.keys()

    for app_name in app_names:
        collaboration_models = \
            apps.get_app_config(app_name).collaboration_models

        for collaboration in collaboration_models:
            module = importlib
            module = \
                module.import_module('colab.proxy.{}.models'.format(app_name))

            module = eval("module." + collaboration['model'])
            elements = module.objects

            if filter_by_user:
                dic = {}
                dic[collaboration['collaborator_username']] = filter_by_user
                elements = elements.filter(**dic)
            else:
                elements = elements.all()

            latest_results.extend(parsePreviewBlock(elements, collaboration))

            if populate_count_types:
                count_types[collaboration['model'].lower()] = elements.count()

    if populate_count_types:
        cache.set('home_chart', count_types, 30)

    for key in count_types.keys():
        count_types[trans(key)] = count_types.pop(key)

    return latest_results, count_types


def parsePreviewBlock(elements, collaboration):
    results = []
    for element in elements:
        previewblock = PreviewBlock()
        attributes = collaboration.keys()

        for keyname in attributes:
            if keyname == 'model' or keyname == 'model_verbose' \
                    or len(collaboration[keyname].strip()) == 0:
                continue
            value = getattr(element, collaboration[keyname])
            if(inspect.ismethod(value)):
                setattr(previewblock, keyname, value())
            else:
                setattr(previewblock, keyname, value)

        results.append(previewblock)

    return results
