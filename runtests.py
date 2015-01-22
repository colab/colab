#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'colab.tests.settings'
os.environ['COVERAGE_PROCESS_START'] = '.coveragerc'
os.environ['REUSE_DB'] = '0'

import django
import coverage

from django.test.utils import get_runner
from django.conf import settings


def runtests():
    if django.VERSION >= (1, 7, 0):
        django.setup()
    test_runner = get_runner(settings)
    failures = test_runner(interactive=False, failfast=False).run_tests([])
    sys.exit(failures)


if __name__ == '__main__':
    if os.path.exists('.coverage'):
        os.remove('.coverage')
    coverage.process_startup()
    runtests()
