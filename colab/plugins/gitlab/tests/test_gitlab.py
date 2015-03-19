"""
Test User class.
Objective: Test parameters, and behavior.
"""
from datetime import datetime


from django.test import TestCase, Client
from colab.accounts.models import User
from colab.plugins.gitlab.models import GitlabProject, \
    GitlabIssue, GitlabComment, GitlabMergeRequest


class GitlabTest(TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.client = Client()
        self.create_gitlab_data()

        super(GitlabTest, self).setUp()

    def tearDown(self):
        pass

    def test_data_integrity(self):
        self.assertEqual(GitlabProject.objects.all().count(), 1)
        self.assertEqual(GitlabMergeRequest.objects.all().count(), 1)
        self.assertEqual(GitlabIssue.objects.all().count(), 1)
        self.assertEqual(GitlabComment.objects.all().count(), 2)

    def test_project_url(self):
        self.assertEqual(GitlabProject.objects.get(id=1).url,
                         '/gitlab/softwarepublico/colab')

    def test_merge_request_url(self):
        self.assertEqual(GitlabMergeRequest.objects.get(id=1).url,
                         '/gitlab/softwarepublico/colab/merge_requests/1')

    def test_issue_url(self):
        self.assertEqual(GitlabIssue.objects.get(id=1).url,
                         '/gitlab/softwarepublico/colab/issues/1')

    def test_comment_on_mr_url(self):
        url = '/gitlab/softwarepublico/colab/merge_requests/1#notes_1'
        self.assertEqual(GitlabComment.objects.get(id=1).url, url)

    def test_comment_on_issue_url(self):
        self.assertEqual(GitlabComment.objects.get(id=2).url,
                         '/gitlab/softwarepublico/colab/issues/1#notes_2')

    def create_gitlab_data(self):
        g = GitlabProject()
        g.id = 1
        g.name = "colab"
        g.name_with_namespace = "Software Public / Colab"
        g.path_with_namespace = "softwarepublico/colab"
        g.created_at = datetime.now()
        g.last_activity_at = datetime.now()
        g.save()

        mr = GitlabMergeRequest()
        mr.id = 1
        mr.project = g
        mr.title = "Include plugin support"
        mr.description = "Merge request for plugin support"
        mr.state = "Closed"
        mr.created_at = datetime.now()
        mr.update_user(self.user.username)
        mr.save()

        i = GitlabIssue()
        i.id = 1
        i.project = g
        i.title = "Issue for colab"
        i.description = "Issue reported to colab"
        i.created_at = datetime.now()
        i.state = "Open"
        i.update_user(self.user.username)
        i.save()

        c1 = GitlabComment()
        c1.id = 1
        c1.parent_id = mr.id
        c1.project = g
        c1.body = "Comment to merge request"
        c1.created_at = datetime.now()
        c1.issue_comment = False
        c1.update_user(self.user.username)
        c1.save()

        c2 = GitlabComment()
        c2.id = 2
        c2.parent_id = i.id
        c2.project = g
        c2.body = "Comment to issue"
        c2.created_at = datetime.now()
        c2.issue_comment = True
        c2.update_user(self.user.username)
        c2.save()

    def create_user(self):
        user = User()
        user.username = "USERtestCoLaB"
        user.set_password("123colab4")
        user.email = "usertest@colab.com.br"
        user.id = 1
        user.twitter = "usertestcolab"
        user.facebook = "usertestcolab"
        user.first_name = "USERtestCoLaB"
        user.last_name = "COLAB"
        user.save()

        return user
