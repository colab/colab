"""
Test Sign Up view
This test related with accounts/views.py
"""

from django.test import TestCase, Client
from colab.accounts.models import User


class TestSignUpView(TestCase):

    def setUp(self):
        self.user = self.create_user_django()
        self.client = Client()

    def tearDown(self):
        self.user.delete()

    def create_user_django(self):
        user = User.objects.create_user("USERtestCoLaB",
                                        "usertest@colab.com.br", "123colab4")
        return user

    def test_user_authenticated_and_unregistered(self):
        self.client.login(username="usertestcolab", password="123colab4")
        response = self.client.get("/account/register/")
        self.assertEquals(200, response.status_code)
        self.client.logout()

    def test_user_authenticated_and_registered(self):
        self.user.needs_update = False
        self.user.save()
        self.client.login(username="usertestcolab", password="123colab4")
        response = self.client.get("/account/register/")
        self.assertEquals(302, response.status_code)
        url = "http://testserver/account/usertestcolab"
        self.assertEquals(url, response.url)
        self.client.logout()
