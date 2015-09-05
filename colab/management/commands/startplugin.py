
import os

import colab

from django.core.management.commands.startapp import Command as StartAppCommand


class Command(StartAppCommand):
    help = ("Creates a Colab plugin directory structure for the given "
            "plugin name in the current directory or optionally in the "
            "plugin directory.")
    missing_args_message = "You must provide a plugin name"

    def handle_template(self, template, subdir):
        if template is None:
            return os.path.join(colab.__path__[0], 'conf', 'plugin_template')

        return super(Command, self).handle_template(template, subdir)

    def handle(self, name, **kwargs):
        kwargs['app_name_dash'] = name.replace('_', '-')
        kwargs['app_name_camel'] = name.title().replace('_', '')
        kwargs['app_name_verbose'] = name.replace('_', ' ').title()
        super(Command, self).handle(name, **kwargs)
