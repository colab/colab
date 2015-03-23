import json
import urllib
import urllib2
import logging

from dateutil.parser import parse

from django.conf import settings
from django.db.models.fields import DateTimeField

from colab.plugins.gitlab.models import (GitlabProject, GitlabMergeRequest,
                                         GitlabComment, GitlabIssue)
from colab.plugins.utils.proxy_data_api import ProxyDataAPI

LOGGER = logging.getLogger('colab.plugin.gitlab')


class GitlabDataAPI(ProxyDataAPI):

    def get_request_url(self, path, **kwargs):
        proxy_config = settings.PROXIED_APPS.get(self.app_label, {})

        upstream = proxy_config.get('upstream')
        kwargs['private_token'] = proxy_config.get('private_token')
        params = urllib.urlencode(kwargs)

        if upstream[-1] == '/':
            upstream = upstream[:-1]

        return u'{}{}?{}'.format(upstream, path, params)

    def get_json_data(self, api_url, page, pages=1000):
        url = self.get_request_url(api_url, per_page=pages,
                                   page=page)

        try:
            data = urllib2.urlopen(url, timeout=10)
            json_data = json.load(data)
        except urllib2.URLError:
            LOGGER.exception("Connection timeout: " + url)
            json_data = []

        return json_data

    def fill_object_data(self, element, _object):
        for field in _object._meta.fields:
            try:
                if field.name == "user":
                    _object.update_user(
                        element["author"]["username"])
                    continue
                if field.name == "project":
                    _object.project_id = element["project_id"]
                    continue

                if isinstance(field, DateTimeField):
                    value = parse(element[field.name])
                else:
                    value = element[field.name]

                setattr(_object, field.name, value)
            except KeyError:
                continue

        return _object

    def fetch_projects(self):
        page = 1
        projects = []

        while True:
            json_data = self.get_json_data('/api/v3/projects/all', page)
            page = page + 1

            if not len(json_data):
                break

            for element in json_data:
                project = GitlabProject()
                self.fill_object_data(element, project)
                projects.append(project)

        return projects

    def fetch_merge_request(self, projects):
        all_merge_request = []

        for project in projects:
            page = 1
            while True:
                url = '/api/v3/projects/{}/merge_requests'.format(project.id)
                json_data_mr = self.get_json_data(url, page)
                page = page + 1

                if len(json_data_mr) == 0:
                    break

                for element in json_data_mr:
                    single_merge_request = GitlabMergeRequest()
                    self.fill_object_data(element, single_merge_request)
                    all_merge_request.append(single_merge_request)

        return all_merge_request

    def fetch_issue(self, projects):
        all_issues = []

        for project in projects:
            page = 1
            while True:
                url = '/api/v3/projects/{}/issues'.format(project.id)
                json_data_issue = self.get_json_data(url, page)
                page = page + 1

                if len(json_data_issue) == 0:
                    break

                for element in json_data_issue:
                    single_issue = GitlabIssue()
                    self.fill_object_data(element, single_issue)
                    all_issues.append(single_issue)

        return all_issues

    def fetch_comments(self):
        all_comments = []
        all_comments.extend(self.fetch_comments_MR())
        all_comments.extend(self.fetch_comments_issues())

        return all_comments

    def fetch_comments_MR(self):
        all_comments = []
        all_merge_requests = GitlabMergeRequest.objects.all()

        for merge_request in all_merge_requests:
            page = 1
            while True:
                url = '/api/v3/projects/{}/merge_requests/{}/notes'.format(
                    merge_request.project_id, merge_request.id)
                json_data_mr = self.get_json_data(url, page)
                page = page + 1

                if len(json_data_mr) == 0:
                    break

                for element in json_data_mr:
                    single_comment = GitlabComment()
                    self.fill_object_data(element, single_comment)
                    single_comment.project = merge_request.project
                    single_comment.issue_comment = False
                    single_comment.parent_id = merge_request.id
                    all_comments.append(single_comment)

        return all_comments

    def fetch_comments_issues(self):
        all_comments = []
        all_issues = GitlabIssue.objects.all()

        for issue in all_issues:
            page = 1
            while True:
                url = '/api/v3/projects/{}/issues/{}/notes'.format(
                    issue.project_id, issue.id)
                json_data_mr = self.get_json_data(url, page)
                page = page + 1

                if len(json_data_mr) == 0:
                    break

                for element in json_data_mr:
                    single_comment = GitlabComment()
                    self.fill_object_data(element, single_comment)
                    single_comment.project = issue.project
                    single_comment.issue_comment = True
                    single_comment.parent_id = issue.id
                    all_comments.append(single_comment)

        return all_comments

    def fetch_data(self):
        LOGGER.info("Importing Projects")
        projects = self.fetch_projects()
        for datum in projects:
            datum.save()

        LOGGER.info("Importing Merge Requests")
        merge_request_list = self.fetch_merge_request(projects)
        for datum in merge_request_list:
            datum.save()

        LOGGER.info("Importing Issues")
        issue_list = self.fetch_issue(projects)
        for datum in issue_list:
            datum.save()

        LOGGER.info("Importing Comments")
        comments_list = self.fetch_comments()
        for datum in comments_list:
            datum.save()

    @property
    def app_label(self):
        return 'gitlab'
