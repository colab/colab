
from datetime import timedelta
from celery.decorators import periodic_task

from .data import TASKS


@periodic_task(run_every=timedelta(seconds=60))
def import_plugin_data():
    for task in TASKS:
        task.delay()
