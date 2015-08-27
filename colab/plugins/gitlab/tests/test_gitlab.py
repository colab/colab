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
        self.assertEqual(GitlabProject.objects.all().count(), 2)
        self.assertEqual(GitlabMergeRequest.objects.all().count(), 2)
        self.assertEqual(GitlabIssue.objects.all().count(), 2)
        self.assertEqual(GitlabComment.objects.all().count(), 2)

    def test_project_url(self):
        self.assertEqual(GitlabProject.objects.get(id=1).url,
                         '/gitlab/softwarepublico/colab')

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

    def create_gitlab_data(self):
        g1 = GitlabProject()
        g1.id = 1
        g1.name = "colab"
        g1.name_with_namespace = "Software Public / Colab"
        g1.path_with_namespace = "softwarepublico/colab"
        g1.created_at = datetime.now()
        g1.last_activity_at = datetime.now()
        g1.save()

        g2 = GitlabProject()
        g2.id = 2
        g2.name = "colabinc"
        g2.name_with_namespace = "Software Public / ColabInc"
        g2.path_with_namespace = "softwarepublico/colabinc"
        g2.created_at = datetime.now()
        g2.last_activity_at = datetime.now()
        g2.save()

        mr1 = GitlabMergeRequest()
        mr1.id = 1
        mr1.iid = 1
        mr1.project = g1
        mr1.title = "Include plugin support"
        mr1.description = "Merge request for plugin support"
        mr1.state = "Closed"
        mr1.created_at = datetime.now()
        mr1.update_user(self.user.username)
        mr1.save()

        mr2 = GitlabMergeRequest()
        mr2.id = 2
        mr2.iid = 1
        mr2.project = g2
        mr2.title = "Include test support"
        mr2.description = "Merge request for test support"
        mr2.state = "Closed"
        mr2.created_at = datetime.now()
        mr2.update_user(self.user.username)
        mr2.save()

        i1 = GitlabIssue()
        i1.id = 1
        i1.iid = 1
        i1.project = g1
        i1.title = "Issue for colab"
        i1.description = "Issue reported to colab"
        i1.created_at = datetime.now()
        i1.state = "Open"
        i1.update_user(self.user.username)
        i1.save()

        i2 = GitlabIssue()
        i2.id = 2
        i2.iid = 1
        i2.project = g2
        i2.title = "Issue for colab"
        i2.description = "Issue reported to colab"
        i2.created_at = datetime.now()
        i2.state = "Open"
        i2.update_user(self.user.username)
        i2.save()

        c1 = GitlabComment()
        c1.id = 1
        c1.parent_id = mr1.iid
        c1.project = g1
        c1.body = "Comment to merge request"
        c1.created_at = datetime.now()
        c1.issue_comment = False
        c1.update_user(self.user.username)
        c1.save()

        c2 = GitlabComment()
        c2.id = 2
        c2.parent_id = i1.id
        c2.project = g1
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
