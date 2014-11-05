
from django.conf import settings 

from feedzilla.management.commands import feedzilla_update


class Command(feedzilla_update.Command):
    def handle(self, *args, **kwargs):
        if getattr(settings, 'FEEDZILLA_ENABLED', False):
            super(Command, self).handle(*args, **kwargs)
