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

    def test_user_authenticated_and_registered_with_post(self):
        self.user.needs_update = False
        self.user.save()
        self.client.login(username="usertestcolab", password="123colab4")
        response = self.client.post("/account/register/")
        self.assertEquals(302, response.status_code)
        url = "http://testserver/account/usertestcolab"
        self.assertEquals(url, response.url)
        self.client.logout()

    def test_signup_with_post_not_success(self):
        data_user = {
            'username': 'username',
            'password1': 'safepassword',
            'password2': 'safepassword',
        }
        before = User.objects.count()
        self.client.post('/account/register', data=data_user)
        after = User.objects.count()
        self.assertEqual(before, after)

    def test_signup_with_post_with_success(self):
        data_user = {
            'username': 'username',
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'mail@mail.com',
            'password1': 'safepassword',
            'password2': 'safepassword',
        }
        before = User.objects.count()
        self.client.post('/account/register', data=data_user)
        after = User.objects.count()
        self.assertEqual(before + 1, after)
