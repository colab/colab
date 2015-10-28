"""
Test User Mailing list Subscriptions class.
Objective: Test parameters, and behavior.
"""

from colab.accounts.models import User
from django.test import TestCase, Client


class UserSubscriptionTest(TestCase):
    OK = 200
    FORBIDDEN_ACCESS = 403

    def setUp(self):
        self.user = self.create_user()
        self.client = Client()

    def tearDown(self):
        pass

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

    def authenticate_user(self):
        self.user.needs_update = False
        self.user.save()
        self.client.login(username=self.user.username,
                          password='123colab4')

    def test_manage_subscription_logged_in(self):
        self.authenticate_user()
        response = self.client.get("/account/" + self.user.username +
                                   "/subscriptions")
        self.assertEqual(response.status_code, self.OK)

    def test_manage_subscription_without_login(self):
        response = self.client.get("/account/" + self.user.username +
                                   "/subscriptions")
        self.assertEqual(response.status_code, self.FORBIDDEN_ACCESS)
