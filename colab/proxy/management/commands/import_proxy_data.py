#!/usr/bin/env python

import importlib

from django.core.management.base import BaseCommand
from django.conf import settings

from colab.proxy.proxybase.proxy_data_api import ProxyDataAPI


class Command(BaseCommand):
    help = "Import proxy data into colab database"

    def handle(self, *args, **kwargs):
        print "Executing extraction command..."

        for module_name in settings.PROXIED_APPS.keys():
            module_path = 'colab.proxy.{}.data_api'.format(module_name)
            module = importlib.import_module(module_path)

            for module_item_name in dir(module):
                module_item = getattr(module, module_item_name)
                if issubclass(module_item, ProxyDataAPI):
                    if module_item != ProxyDataAPI:
                        api = module_item()
                        api.fetchData()
