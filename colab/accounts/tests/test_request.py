"""
Test account redirections.
Objective: Test requests.
"""

from django.test import TestCase, Client
from django.test.client import RequestFactory
from colab.accounts.models import User


class RequestTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_successful_signup(self):
        # TODO
        pass

    def test_invalid_user_profile_url(self):
        response = self.client.get('/account/johndoe/')
        self.assertEqual(404, response.status_code)

    def test_valid_user_profile_url(self):
        self.userTest = User()
        self.userTest.username = "usertest"
        self.userTest.email = "usertest@colab.com.br"
        self.userTest.set_password("1234colab")
        self.userTest.save()
        response = self.client.get('/account/usertest/')
        self.assertEqual(200, response.status_code)

    def test_valid_login_url(self):
        response = self.client.get('/account/login')
        self.assertEqual(200, response.status_code)
