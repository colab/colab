"""
Test User class.
Objective: Test parameters, and behavior.
"""
from datetime import datetime
from django.test import TestCase, Client
from colab.plugins.gitlab.models import (GitlabProject, GitlabGroup,
                                         GitlabIssue, GitlabComment,
                                         GitlabMergeRequest)


class GitlabTest(TestCase):

    fixtures = ['test_gitlab_data']

    def setUp(self):
        self.client = Client()

        super(GitlabTest, self).setUp()

    def tearDown(self):
        pass

    def test_data_integrity(self):
        self.assertEqual(GitlabGroup.objects.all().count(), 1)
        self.assertEqual(GitlabProject.objects.all().count(), 2)
        self.assertEqual(GitlabMergeRequest.objects.all().count(), 2)
        self.assertEqual(GitlabIssue.objects.all().count(), 2)
        self.assertEqual(GitlabComment.objects.all().count(), 2)

    def test_project_url(self):
        self.assertEqual(GitlabProject.objects.get(id=1).url,
                         '/gitlab/softwarepublico/colab')

    def test_project_group(self):
        project = GitlabProject.objects.get(id=1)
        self.assertEqual(project.name, 'colab')
        self.assertEqual(project.namespace, 'softwarepublico')

    def test_namespace_projects(self):
        group = GitlabGroup.objects.get(id=1)
        self.assertEqual(len(group.projects), 2)
        self.assertEqual(group.projects[0].name, 'colab')
        self.assertEqual(group.projects[1].name, 'colabinc')

    def test_merge_request_url(self):
        self.assertEqual(GitlabMergeRequest.objects.get(id=1).url,
                         '/gitlab/softwarepublico/colab/merge_requests/1')
        self.assertEqual(GitlabMergeRequest.objects.get(id=2).url,
                         '/gitlab/softwarepublico/colabinc/merge_requests/1')

    def test_issue_url(self):
        self.assertEqual(GitlabIssue.objects.get(id=1).url,
                         '/gitlab/softwarepublico/colab/issues/1')
        self.assertEqual(GitlabIssue.objects.get(id=2).url,
                         '/gitlab/softwarepublico/colabinc/issues/1')

    def test_comment_on_mr_url(self):
        url = '/gitlab/softwarepublico/colab/merge_requests/1#notes_1'
        self.assertEqual(GitlabComment.objects.get(id=1).url, url)

    def test_comment_on_issue_url(self):
        self.assertEqual(GitlabComment.objects.get(id=2).url,
                         '/gitlab/softwarepublico/colab/issues/1#notes_2')
