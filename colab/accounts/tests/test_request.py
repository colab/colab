"""
Test account redirections.
Objective: Test requests.
"""

from django.test import TestCase, Client
from django.test.client import RequestFactory
from colab.accounts.models import User
from colab.accounts.context_processors import social_network_enabled
from django.conf import settings


class RequestTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_successful_signup(self):
        # TODO
        pass

    def create_user(self):
        self.user_test = User()
        self.user_test.username = "usertest"
        self.user_test.email = "usertest@colab.com.br"
        self.user_test.set_password("1234colab")
        self.user_test.save()

    def test_invalid_user_profile_url(self):
        response = self.client.get('/account/johndoe/')
        self.assertEqual(404, response.status_code)

    def test_valid_user_profile_url(self):
        self.create_user()
        response = self.client.get('/account/usertest/')
        self.assertEqual(200, response.status_code)

    def test_valid_login_url(self):
        response = self.client.get('/account/login')
        self.assertEqual(200, response.status_code)

    def test_myaccount_redirect_not_authenticated_user(self):
        self.create_user()
        response = self.client.get('/myaccount/edit')
        self.assertEqual(404, response.status_code)

    def test_myaccount_redirect_user_profile(self):
        self.create_user()
        self.client.login(username="usertest", password='1234colab')
        response = self.client.get('/myaccount/')
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://testserver/account/usertest/", response.url)

    def test_myaccount_redirect_edit(self):
        self.create_user()
        self.client.login(username="usertest", password='1234colab')
        response = self.client.get('/myaccount/edit')
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://testserver/account/usertest/edit",
                         response.url)

    def test_myaccount_redirect_subscriptions(self):
        self.create_user()
        self.client.login(username="usertest", password='1234colab')
        response = self.client.get('/myaccount/subscriptions')
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://testserver/account/usertest/subscriptions",
                         response.url)


class SocialNetworkTest(TestCase):
    """docstring for SocialNetworkTest"""

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def create_user(self):
        self.user_test = User()
        self.user_test.username = "usertest"
        self.user_test.email = "usertest@colab.com.br"
        self.user_test.set_password("1234colab")
        self.user_test.save()

    def test_social_network(self):
        self.create_user()
        self.client.login(username="usertest", password='1234colab')
        response = self.client.get('/myaccount/')
        result = social_network_enabled(response)['SOCIAL_NETWORK_ENABLED']
        self.assertTrue(result)
        self.assertTrue(settings.SOCIAL_NETWORK_ENABLED)
