from django.test import TestCase
from django.test.utils import override_settings
from ..data_importer import GitlabDataImporter
from ..models import GitlabProject
from mock import patch
import data


class GitlabDataImporterTest(TestCase):

    fixtures = ["gitlab_associations"]

    colab_apps = data.colab_apps
    projects_json = data.projects_json
    groups_json = data.groups_json
    merge_json = data.merge_json

    @override_settings(COLAB_APPS=colab_apps)
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
        mock_json.side_effect = [self.projects_json, []]

        projects = self.api.fetch_projects()
        self.assertEqual(len(projects), 1)

        self.assertEqual(projects[0].description, "Test Gitlab")
        self.assertEqual(projects[0].public, True)

    @patch.object(GitlabDataImporter, 'get_json_data')
    def test_fetch_groups(self, mock_json):
        mock_json.side_effect = [self.groups_json, []]

        groups = self.api.fetch_groups()
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0].name, "Group 1")
        self.assertEqual(groups[1].name, "Group 2")

        self.assertEqual(groups[0].path, "group-1")
        self.assertEqual(groups[1].path, "group-2")

    @patch.object(GitlabDataImporter, 'get_json_data')
    def test_fetch_merge(self, mock_json):
        mock_json.side_effect = [self.merge_json, []]

        merges = self.api.fetch_merge_request([GitlabProject()])
        self.assertEqual(len(merges), 1)
        self.assertEqual(merges[0].title, "Merge Title")
        self.assertEqual(merges[0].description, "description")
        self.assertEqual(merges[0].get_author().username, "user")
