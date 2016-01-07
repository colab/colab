from django.test import TestCase
from colab.accounts.models import User
from colab.plugins.utils.models import Collaboration


class CollaborationTest(TestCase):
    fixtures = ['sample_user_plugin.json']

    def setUp(self):
        self.collaboration = Collaboration()

    def set_user(self):
        sample_user = User.objects.filter(username='SampleUser').last()
        self.collaboration.user = sample_user

    def test_modified_by_without_user(self):
        self.assertIsNone(self.collaboration.modified_by)

    def test_modified_by_with_valid_user(self):
        self.set_user()
        self.assertEqual('SampleUser LastName', self.collaboration.modified_by)

    def test_modified_by_url_without_user(self):
        self.assertIsNone(self.collaboration.modified_by_url)

    def test_modified_by_url_with_valid_user(self):
        self.set_user()
        self.assertEquals('/account/SampleUser',
                          self.collaboration.modified_by_url)

    def test_update_user_without_user(self):
        self.collaboration.update_user('SampleInvalidUser')
        self.assertIsNone(self.collaboration.user)

    def test_update_user_with_valid_user(self):
        self.collaboration.update_user('SampleUser')
        self.assertEquals('SampleUser', self.collaboration.user.username)
        self.assertEquals('sample_user@email.com',
                          self.collaboration.user.email)
