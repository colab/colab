#!/bin/bash

export DJANGO_SETTINGS_MODULE="colab.tests.settings"

django-admin test
