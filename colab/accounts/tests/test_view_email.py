"""
Test Email view
This test related with accounts/views.py
"""

from django.test import TestCase, Client
from colab.accounts.models import User


class TestEmailView(TestCase):

    def setUp(self):
        self.user = self.create_user_django()
        self.client = Client()

    def tearDown(self):
        self.user.delete()

    def create_user_django(self):
        user = User.objects.create_user("USERtestCoLaB",
                                        "usertest@colab.com.br", "123colab4")
        return user

    def authenticate_user(self):
        self.client.login(username=self.user.username,
                          password="123colab4")

    def test_user_update_add_other_valid_email(self):
        self.authenticate_user()
        email = "usertest2@colab.com.br"
        response = self.client.post('/account/manage/email/' +
                                    str(self.user.id),
                                    {'email': email, 'id': self.user.id},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(201, response.status_code)
        self.client.logout()

    def test_user_update_add_invalid_email(self):
        self.authenticate_user()
        invalid_email = "e"
        response = self.client.post('/account/manage/email/' +
                                    str(self.user.id),
                                    {'email': invalid_email,
                                        'id': self.user.id},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # 400 is the bad request error
        self.assertEquals(400, response.status_code)
        self.client.logout()

    def test_user_update_add_blank_email(self):
        self.authenticate_user()
        blank_email = ""
        response = self.client.post('/account/manage/email/' +
                                    str(self.user.id),
                                    {'email': blank_email, 'id': self.user.id},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # 400 is the bad request error
        self.assertEquals(400, response.status_code)
        self.client.logout()
