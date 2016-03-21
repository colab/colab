#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'colab.settings'
os.environ['COLAB_SETTINGS'] = 'tests/colab_settings.py'
os.environ['COLAB_SETTINGS_DIR'] = 'tests/settings.d'
os.environ['COLAB_WIDGETS_SETTINGS'] = 'tests/widgets_settings.py'
os.environ['COLAB_PLUGINS'] = 'tests/plugins.d'
os.environ['COLAB_WIDGETS'] = 'tests/widgets.d'
os.environ['COVERAGE_PROCESS_START'] = '.coveragerc'

import coverage

# Needs to come before the settings import, because some settings instantiate
# objetcs. If they are executed before the coverage startup, those lines
# won't be covered.
if os.path.exists('.coverage'):
    os.remove('.coverage')
coverage.process_startup()

import django
from django.conf import settings
from django.test.utils import get_runner
import colab.settings


def runtests(test_suites=[]):
    if django.VERSION >= (1, 7, 0):
        django.setup()

    test_runner = get_runner(settings)
    failures = test_runner(interactive=False, failfast=False).run_tests(
        test_suites)
    sys.exit(failures)


if __name__ == '__main__':
    all_valid_apps = True

    for arg in sys.argv[1:]:
        if arg not in colab.settings.INSTALLED_APPS:
            print arg + " App not found"
            print "Try colab." + arg
            all_valid_apps = False

    if all_valid_apps:
        runtests(sys.argv[1:])
