#!/usr/bin/env python

import colab
from django.core.management.base import BaseCommand
from colab.super_archives.models import Message
from django.conf import settings
modules = [ i for i in settings.INSTALLED_APPS if i.startswith("colab.proxy.") ]
for module in modules:
  module += ".data_api"
  __import__(module, locals(), globals())

class Command(BaseCommand):
    help = "Import proxy data into colab database"

    def handle(self, *args, **kwargs):
        print "Executing extraction command..."

        for module in modules:
          extractionClassname = module + ".data_api." + module.split('.')[-1].title() + "DataAPI"
          api = eval(extractionClassname)()
          api.fetchData()
