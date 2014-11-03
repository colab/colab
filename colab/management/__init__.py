
import os

from django.core.management import ManagementUtility

from .initconfig import initconfig


def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colab.settings")

    utility = ManagementUtility(argv)
    utility.execute()


def run_colab_config(argv=None):
    initconfig()
