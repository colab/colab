import json
import urllib
import urllib2
import logging

from dateutil.parser import parse

from django.db.models.fields import DateTimeField
from colab.plugins.data import PluginDataImporter

from .models import (GitlabProject, GitlabMergeRequest,
                     GitlabComment, GitlabIssue, GitlabGroup)


LOGGER = logging.getLogger('colab.plugin.gitlab')


class GitlabDataImporter(PluginDataImporter):
    app_label = 'gitlab'

    def get_request_url(self, path, **kwargs):
        upstream = self.config.get('upstream')
        kwargs['private_token'] = self.config.get('private_token')
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

    def fetch(self, url, gitlab_class):
        page = 1
        obj_list = []

        while True:
            json_data = self.get_json_data(url, page)
            page = page + 1

            if not len(json_data):
                break

            for element in json_data:
                obj = gitlab_class()
                self.fill_object_data(element, obj)
                obj_list.append(obj)

        return obj_list

    def fetch_comments(self, url, parent_class, issue_comment):
        all_comments = []
        all_parent_objects = parent_class.objects.all()

        for parent_obj in all_parent_objects:
            page = 1
            while True:
                formated_url = url.format(parent_obj.project_id, parent_obj.id)
                json_data = self.get_json_data(formated_url, page)
                page = page + 1

                if len(json_data) == 0:
                    break

                for element in json_data:
                    single_comment = GitlabComment()
                    self.fill_object_data(element, single_comment)
                    single_comment.project = parent_obj.project
                    single_comment.issue_comment = issue_comment
                    single_comment.parent_id = parent_obj.id
                    all_comments.append(single_comment)

        return all_comments

    def fetch_projects(self):
        return self.fetch('/api/v3/projects/all', GitlabProject)

    def fetch_groups(self):
        return self.fetch('/api/v3/groups', GitlabGroup)

    def fetch_merge_request(self, projects):
        merge_requests = []
        for project in projects:
            url = '/api/v3/projects/{}/merge_requests'.format(project.id)
            merge_requests.extend(self.fetch(url, GitlabMergeRequest))
        return merge_requests

    def fetch_issue(self, projects):
        issues = []
        for project in projects:
            url = '/api/v3/projects/{}/issues'.format(project.id)
            issues.extend(self.fetch(url, GitlabIssue))
        return issues

    def fetch_all_comments(self):
        all_comments = []
        all_comments.extend(self.fetch_comments_mr())
        all_comments.extend(self.fetch_comments_issues())

        return all_comments

    def fetch_comments_mr(self):
        url = '/api/v3/projects/{}/merge_requests/{}/notes'
        return self.fetch_comments(url, GitlabMergeRequest, False)

    def fetch_comments_issues(self):
        url = '/api/v3/projects/{}/issues/{}/notes'
        return self.fetch_comments(url, GitlabIssue, True)


class GitlabProjectImporter(GitlabDataImporter):

    def fetch_data(self):
        LOGGER.info("Importing Projects")
        projects = self.fetch_projects()
        for datum in projects:
            datum.save()


class GitlabMergeRequestImporter(GitlabDataImporter):

    def fetch_data(self):
        LOGGER.info("Importing Merge Requests")
        projects = GitlabProject.objects.all()
        merge_request_list = self.fetch_merge_request(projects)
        for datum in merge_request_list:
            datum.save()


class GitlabIssueImporter(GitlabDataImporter):

    def fetch_data(self):
        LOGGER.info("Importing Issues")
        projects = GitlabProject.objects.all()
        issue_list = self.fetch_issue(projects)
        for datum in issue_list:
            datum.save()


class GitlabCommentImporter(GitlabDataImporter):

    def fetch_data(self):
        LOGGER.info("Importing Comments")
        comments_list = self.fetch_all_comments()
        for datum in comments_list:
            datum.save()
