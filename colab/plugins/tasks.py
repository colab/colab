
from datetime import timedelta
from celery.decorators import periodic_task

from .utils import data


@periodic_task(run_every=timedelta(minutes=1))
def import_plugin_data():
    for task in data.TASKS:
        task.delay()
