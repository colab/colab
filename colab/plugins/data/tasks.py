#!/usr/bin/env python

import importlib
import logging

from django.conf import settings

from colab.celery import app

LOGGER = logging.getLogger('colab.plugins.data')
TASKS = set()


def lock(method, name):
    def wrapped_method(self, *args, **kwargs):
        lock_id = 'colab-data-importer-{}'.format(name)
        lock = app.backend.client.lock(lock_id)

        if lock.acquire(blocking=False):
            try:
                return method(*args, **kwargs)
            finally:
                lock.release()

    return wrapped_method


def register_tasks():

    global TASKS

    for app_name in settings.INSTALLED_APPS:

        module_name = '{}.data_importer'.format(app_name)
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue

        for item_name in dir(module):
            item = getattr(module, item_name)

            if callable(getattr(item, 'fetch_data', None)):
                if getattr(item.fetch_data, 'is_abstract', False):
                    continue
                instance = item()
                task_name = '{}.{}'.format(module.__name__, item_name)
                thread_safe_method = lock(instance.fetch_data, task_name)
                task = app.task(name=task_name, bind=True)(thread_safe_method)
                TASKS.add(task)
                LOGGER.debug('Registered task: %s', task_name)

    LOGGER.debug(TASKS)
    return TASKS


def data_import(self):
    for task in TASKS:
        task.delay()
