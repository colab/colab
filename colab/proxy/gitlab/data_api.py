from colab.proxy.gitlab.models import *
from colab.proxy.proxybase.proxy_data_api import ProxyDataAPI
from django.db.models.fields import DateTimeField
from dateutil.parser import parse
import urllib2
import json
from django.conf import settings

class GitlabDataAPI(ProxyDataAPI):


  def fetchProjects(self):
    page = 1
    projects = []

    proxy_config = settings.PROXIED_APPS.get(self.app_label, {})
    admin_token = proxy_config.get('auth_token')

    # Iterates throughout all projects pages
    while(True):
      data = urllib2.urlopen(proxy_config.get('upstream')+'api/v3/projects/all?private_token={}&per_page=100&page={}'.format(admin_token, page))
      json_data = json.load(data)

      if len(json_data) == 0:
        break

      page = page + 1

      for element in json_data:
        project = GitlabProject()

        for field in GitlabProject._meta.fields:
          value = element[field.name]
          value = parse(element[field.name]) if isinstance(field, DateTimeField) else value
          setattr(project, field.name, value)

        projects.append(project)

    return projects


  def fetchData(self):
    data = self.fetchProjects()

    for datum in data:
      datum.save()

  @property
  def app_label(self):
    return 'gitlab'

