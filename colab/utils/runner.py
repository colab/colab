
import os
import sys

from django.core.management import ManagementUtility
from colab.management.commands import initconfig


def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colab.settings")
    from django.conf import settings

    if not hasattr(settings, 'SECRET_KEY') and 'initconfig' in sys.argv:
        command = initconfig.Command()
        command.handle()
    else:
        utility = ManagementUtility(argv)
        utility.execute()
