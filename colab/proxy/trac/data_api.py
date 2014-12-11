from colab.proxy.gitlab.models import *
from colab.proxy.proxybase.proxy_data_api import ProxyDataAPI
from django.db.models.fields import DateTimeField
from dateutil.parser import parse
import urllib2
import json

class TracDataAPI(ProxyDataAPI):

  def fetchData(self):
    pass

