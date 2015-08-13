#!/usr/bin/env python

import importlib

from django.conf import settings

from colab.celery import app
from proxy_data_api import ProxyDataAPI


TASKS = set()


def register_tasks():

    global TASKS

    for app_name in settings.INSTALLED_APPS:

        try:
            module = importlib.import_module('{}.data_api'.format(app_name))
        except ImportError as e:
            continue

        for item_name in dir(module):
            item = getattr(module, item_name)
            if item is ProxyDataAPI:
                continue

            if callable(getattr(item, 'fetch_data', None)):
                instance = item()
                task = app.task(bind=True)(instance.fetch_data)
                TASKS.add(task)

    return TASKS


def data_import(self):
    for task in TASKS:
        task.delay()
