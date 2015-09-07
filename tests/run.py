#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'colab.settings'
os.environ['COLAB_SETTINGS'] = 'tests/colab_settings.py'
os.environ['COLAB_WIDGETS_SETTINGS'] = 'tests/widgets_settings.py'
os.environ['COLAB_PLUGINS'] = 'tests/plugins.d'
os.environ['COLAB_WIDGETS'] = 'tests/widgets.d'
os.environ['COVERAGE_PROCESS_START'] = '.coveragerc'


import django
import coverage

from django.conf import settings
from django.test.utils import get_runner


def runtests():
    if django.VERSION >= (1, 7, 0):
        django.setup()

    test_runner = get_runner(settings)
    failures = test_runner(interactive=False, failfast=False).run_tests([])
    sys.exit(failures)


def run_with_coverage():
    if os.path.exists('.coverage'):
        os.remove('.coverage')
    coverage.process_startup()
    runtests()


if __name__ == '__main__':
    run_with_coverage()
