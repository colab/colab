import json
import urllib
import urllib2

from dateutil.parser import parse

from django.conf import settings
from django.db.models.fields import DateTimeField

from colab.proxy.gitlab.models import GitlabProject
from colab.proxy.utils.proxy_data_api import ProxyDataAPI


class GitlabDataAPI(ProxyDataAPI):

    def get_request_url(self, path, **kwargs):
        proxy_config = settings.PROXIED_APPS.get(self.app_label, {})

        upstream = proxy_config.get('upstream')
        kwargs['private_token'] = proxy_config.get('private_token')
        params = urllib.urlencode(kwargs)

        if upstream[-1] == '/':
            upstream = upstream[:-1]

        return u'{}{}?{}'.format(upstream, path, params)

    def fetchProjects(self):
        page = 1
        projects = []

        # Iterates throughout all projects pages
        while(True):
            url = self.get_request_url('/api/v3/projects/all',
                                       per_page=100,
                                       page=page)
            data = urllib2.urlopen(url)
            json_data = json.load(data)

            if len(json_data) == 0:
                break

            page = page + 1

            for element in json_data:
                project = GitlabProject()

                for field in GitlabProject._meta.fields:
                    if isinstance(field, DateTimeField):
                        value = parse(element[field.name])
                    else:
                        value = element[field.name]

                    setattr(project, field.name, value)

                projects.append(project)

        return projects

    def fetch_data(self):
        data = self.fetchProjects()

        for datum in data:
            datum.save()

    @property
    def app_label(self):
        return 'gitlab'
