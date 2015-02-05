import json
import urllib
import urllib2

from dateutil.parser import parse

from django.conf import settings
from django.db.models.fields import DateTimeField

from colab.proxy.gitlab.models import GitlabProject, GitlabMergeRequest
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

    def fetch_projects(self):
        page = 1
        projects = []

        # Iterates throughout all projects pages
        while(True):
            url = self.get_request_url('/api/v3/projects/all',
                                       per_page=1000,
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

#    def fetch_merge_request(self, projects):
#        page = 1
#        all_merge_request = []
#
#        # Iterate under all projects
#        for project in projects:
#            # Iterate under all MR inside project
#            while(True):
#                merge_request_url = \
#                    '/api/v3/projects/{}/merge_requests'.format(project.id)
#                url = self.get_request_url(merge_request_url,
#                                           per_page=1000,
#                                           page=page)
#
#                data = urllib2.urlopen(url)
#                json_data_mr = json.load(data)
#
#                if len(json_data_mr) == 0:
#                    break
#
#                page = page + 1
#                for element in json_data_mr:
#                    single_merge_request = GitlabMergeRequest()
#
#                    for field in GitlabMergeRequest._meta.fields:
#                        if field.name == "user":
#                            single_merge_request.update_user(
#                                element["author"]["username"])
#                            continue
#                        if field.name == "project":
#                            single_merge_request.project_id = \
#                                element["project_id"]
#                            continue
#
#                        if isinstance(field, DateTimeField):
#                            value = parse(element[field.name])
#                        else:
#                            value = element[field.name]
#
#                        setattr(single_merge_request, field.name, value)
#
#                    all_merge_request.append(single_merge_request)
#
#        return all_merge_request

    def fetch_issue(self, projects):
        page = 1
        all_issues = []

        # Iterate under all projects
        for project in projects:
            # Iterate under all Issues inside project
            while(True):
                issue_url = \
                    '/api/v3/projects/{}/issues'.format(project.id)
                url = self.get_request_url(issue_url, per_page=1000,
                                           page=page)

                data = urllib2.urlopen(url)
                json_data_issue = json.load(data)

                if len(json_data_issue) == 0:
                    break

                page = page + 1
                for element in json_data_issue:
                    single_issue = GitlabIssue()

                    for field in GitlabIssue._meta.fields:
                        if field.name == "project":
                            single_issue.project_id = element["project_id"]
                            continue

                        if isinstance(field, DateTimeField):
                            value = parse(element[field.name])
                        else:
                            value = element[field.name]

                        setattr(single_issue, field.name, value)

                    all_issues.append(single_issue)

            return all_issues

    def fetch_data(self):
        data = self.fetch_projects()
        #merge_request_list = self.fetch_merge_request(data)
        issue_list = self.fetch_issue(data)

        for datum in data:
            datum.save()
#        for datum in merge_request_list:
#            datum.save()
        for datum in issue_list:
            datum.save()

    @property
    def app_label(self):
        return 'gitlab'
