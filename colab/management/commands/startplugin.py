
import os

import colab

from django.core.management.commands.startapp import Command as StartAppCommand
from django.core.management.base import CommandError


class Command(StartAppCommand):
    help = ("Creates a Colab plugin directory structure for the given "
            "plugin name in the current directory or optionally in the "
            "plugin directory.")
    missing_args_message = "You must provide a plugin name"

    def handle_template(self, template, subdir):
        return os.path.join(colab.__path__[0], 'conf', 'plugin_template')

    def handle(self, app_name=None, target=None, **options):
        if app_name is None or app_name == "":
            # XXX: remove this when update django to 1.8 or higher
            raise CommandError(self.missing_args_message)

        options['app_name_dash'] = app_name.replace('_', '-')
        options['app_name_camel'] = app_name.title().replace('_', '')
        options['app_name_verbose'] = app_name.replace('_', ' ').title()

        super(Command, self).handle(app_name, target, **options)
