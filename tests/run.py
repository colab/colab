#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'colab.settings'
os.environ['COLAB_SETTINGS'] = 'tests/colab_settings.py'
os.environ['COLAB_PLUGINS'] = 'tests/plugins.d'
os.environ['COVERAGE_PROCESS_START'] = '.coveragerc'


import django
import coverage

from django.conf import settings
from django.core.management import execute_from_command_line
from django.test.utils import get_runner


def runtests():
    if django.VERSION >= (1, 7, 0):
        django.setup()

    test_runner = get_runner(settings)
    failures = test_runner(interactive=False, failfast=False).run_tests([])
    execute_from_command_line(['colab-admin', 'behave'])
    sys.exit(failures)


def run_with_coverage():
    if os.path.exists('.coverage'):
        os.remove('.coverage')
    coverage.process_startup()
    runtests()


if __name__ == '__main__':
    run_with_coverage()
