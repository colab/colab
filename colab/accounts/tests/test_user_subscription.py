"""
Test User Mailing list Subscriptions class.
Objective: Test parameters, and behavior.
"""

from mock import patch
from colab.accounts.models import User
from django.test import TestCase, Client
from colab.accounts.utils import mailman


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

    def authenticate_user(self, user=None, password='123colab4'):
        if not user:
            user = self.user
        user.needs_update = False
        user.save()
        self.client.login(username=user.username,
                          password=password)

    def test_manage_subscription_logged_in(self):
        self.authenticate_user()
        response = self.client.get("/account/" + self.user.username +
                                   "/subscriptions")
        self.assertEqual(response.status_code, self.OK)

    def test_manage_subscription_without_login(self):
        response = self.client.get("/account/" + self.user.username +
                                   "/subscriptions")
        self.assertEqual(response.status_code, self.FORBIDDEN_ACCESS)

    @patch.object(mailman, 'all_lists')
    @patch.object(mailman, 'mailing_lists')
    def test_context_data_generation(self, mailing_lists, all_lists):
        data_user = {
            'username': 'username1',
            'first_name': 'first name1',
            'last_name': 'last name1',
            'email': 'mail1@mail.com',
            'password1': 'safepassword',
            'password2': 'safepassword',
        }
        self.client.post('/account/register', data=data_user)
        user1 = User.objects.last()
        user1.is_active = True
        user1.save()
        self.authenticate_user(user1, 'safepassword')

        mail_lists = [
            {"listname": "name_mock_1", "description": "descript_1"},
            {"listname": "name_mock_2", "description": "descript_2"},
            {"listname": "name_mock_3", "description": "descript_3"},
        ]
        all_lists.return_value = mail_lists

        my_mail_lists = [
            "name_mock_1",
            "name_mock_3",
        ]
        mailing_lists.return_value = my_mail_lists
        response = self.client.get("/account/" + user1.username +
                                   "/subscriptions")
        self.assertEqual(response.status_code, self.OK)
        mailresponse = response.context_data['membership'][user1.email]
        mailresponse = map(lambda x: x[-1], mailresponse)
        expected_value = [True, False, True]
        self.assertEqual(mailresponse, expected_value)
