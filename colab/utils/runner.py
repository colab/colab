
import os

from django.core.management import ManagementUtility


def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colab.settings")

    utility = ManagementUtility(argv)
    utility.execute()
