from django.test import TestCase
from django.test.utils import override_settings
from ..data_importer import GitlabDataImporter
from ..models import GitlabProject, GitlabIssue
from mock import patch
import data
from dateutil.parser import parse


class GitlabDataImporterTest(TestCase):

    fixtures = ["gitlab_associations"]

    @override_settings(COLAB_APPS=data.colab_apps)
    def setUp(self):
        self.api = GitlabDataImporter()

    def test_resquest_url(self):
        url = self.api.get_request_url('/gitlab/test/')
        expected = 'localhost/gitlab/test/?private_token=token'
        self.assertEqual(url, expected)

    def test_resquest_url_with_params(self):
        url = self.api.get_request_url('/gitlab/test/', param='param')
        expected = 'localhost/gitlab/test/?private_token=token&param=param'
        self.assertEqual(url, expected)

    @patch.object(GitlabDataImporter, 'get_json_data')
    def test_fetch_projects(self, mock_json):
        mock_json.side_effect = [data.projects_json, []]

        projects = self.api.fetch_projects()
        self.assertEqual(len(projects), 1)

        self.assertEqual(projects[0].description, "Test Gitlab")
        self.assertEqual(projects[0].public, True)

    @patch.object(GitlabDataImporter, 'get_json_data')
    def test_fetch_groups(self, mock_json):
        mock_json.side_effect = [data.groups_json, []]

        groups = self.api.fetch_groups()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0].name, "Group 1")
        self.assertEqual(groups[1].name, "Group 2")

        self.assertEqual(groups[0].path, "group-1")
        self.assertEqual(groups[1].path, "group-2")

    @patch.object(GitlabDataImporter, 'get_json_data')
    def test_fetch_merge(self, mock_json):
        mock_json.side_effect = [data.merge_json, []]

        merges = self.api.fetch_merge_request([GitlabProject()])
        self.assertEqual(len(merges), 1)
        self.assertEqual(merges[0].title, "Merge Title")
        self.assertEqual(merges[0].description, "description")
        self.assertEqual(merges[0].get_author().username, "user")

    @patch.object(GitlabDataImporter, 'get_json_data')
    def test_fetch_issues(self, mock_json):
        mock_json.side_effect = [data.issues_json, []]

        issues = self.api.fetch_issue([GitlabProject()])
        assert mock_json.called
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].title, "title")
        self.assertEqual(issues[0].description, "description")
        self.assertEqual(issues[0].state, "opened")

    @patch.object(GitlabDataImporter, 'get_json_data')
    def test_fetch_comments_mr(self, mock_json):
        mock_json.side_effect = [data.comment_mr_json, []]

        comments_mr = self.api.fetch_comments_mr()
        self.assertEqual(len(comments_mr), 1)
        self.assertEqual(comments_mr[0].body, "message body")
        self.assertEqual(comments_mr[0].user.username, "user")

    @patch.object(GitlabDataImporter, 'get_json_data')
    def test_fetch_comments_issues(self, mock_json):
        mock_json.side_effect = [data.comment_issue_json, []]

        comments_issue = self.api.fetch_comments_issues()
        self.assertEqual(len(comments_issue), 1)
        self.assertEqual(comments_issue[0].body, "message body")
        self.assertEqual(comments_issue[0].user.username, "user")

    def test_fill_object_data(self):
        issue = GitlabIssue()

        self.api.fill_object_data(data.issues_json[0], issue)
        self.assertIsNotNone(issue.user)
        self.assertEqual(issue.user.username, "user")
        self.assertEqual(issue.created_at, parse("2014-10-11T16:25:37.548Z"))
        self.assertEqual(issue.project_id, 32)
        self.assertEqual(issue.title, "title")
