# -*- coding:utf-8 -*-

from mock import patch

from colab.accounts.models import User
from django.test import TestCase
from colab.super_archives.models import EmailAddress


class SignalsTest(TestCase):
    def setUp(self):
        self.user = self.create_user()

    def create_user(self):
        user = User()
        user.username = "USERtestCoLaB"
        user.set_password("123colab4")
        user.email = "usertest@colab.com.br"
        user.id = 1
        user.first_name = "USERtestCoLaB"
        user.last_name = "COLAB"
        user.save()

        return user

    #TODO: see colab/accounts/models.py before uncomment this lines
    #@patch.object(User, 'update_subscription')
    #def test_delete_user_without_email(self, update_subscription_mock):
    #    update_subscription_mock.return_value = True
    #    self.user.delete()
    #    self.assertEqual(0, update_subscription_mock.call_count)

    #@patch.object(User, 'update_subscription')
    #def test_delete_user_with_email(self, update_subscription_mock):
    #    update_subscription_mock.return_value = True

    #    EmailAddress.objects.get_or_create(user=self.user,
    #                                       address="usertest@colab.com.br")
    #    EmailAddress.objects.get_or_create(user=self.user,
    #                                       address="teste@gmail.com")

    #    self.user.delete()
    #    self.assertEqual(2, update_subscription_mock.call_count)
    #    self.assertEqual(0, EmailAddress.objects.count())
