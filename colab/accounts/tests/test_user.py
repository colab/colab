"""
Test User class.
Objective: Test parameters, and behavior.
"""
from colab.accounts.models import User
from django.test import TestCase


class UserTest(TestCase):

    def setUp(self):
        self.user = self.create_user()

    def create_user(self):
        user = User()
        user.username = "USERtestCoLaB"
        user.set_password("123colab4")
        user.email = "usertest@colab.com.br"
        user.id = 1
        user.twitter = "usertestcolab"
        user.facebook = "usertestcolab"
        user.save()

        return user

    def test_check_password(self):
        self.assertTrue(self.user.check_password("123colab4"))
        self.assertFalse(self.user.check_password("1234"))

    def test_get_absolute_url(self):
        url = self.user.get_absolute_url()
        self.assertEqual("/account/usertestcolab", url)

    def test_twitter_link(self):
        link_twitter = self.user.twitter_link()
        self.assertEqual('https://twitter.com/usertestcolab', link_twitter)

    def test_facebook_link(self):
        link_facebook = self.user.facebook_link()
        self.assertEqual('https://www.facebook.com/usertestcolab',
                         link_facebook)

    def test_mailinglists(self):
        empty_list = ()
        self.assertEqual(empty_list, self.user.mailinglists())

    def test_update_subscription(self):
        pass
        # TODO: You should have mailman connection.

    def test_save(self):
        username_test = "USERtestCoLaB"

        user_db = User.objects.get(id=1)
        self.assertEqual(user_db.username, username_test.lower())
        self.user.delete()
