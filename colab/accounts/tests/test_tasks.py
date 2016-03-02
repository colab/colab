
import mock

from colab.accounts.models import User
from colab.accounts import forms as accounts_forms
from django.test import TestCase, Client, override_settings
from datetime import timedelta
from time import sleep

from colab.accounts.tasks import account_verification


class TasksTest(TestCase):

    def create_user(self,name='samplename', email='test@email.com',
                    is_active=True):
        user = User()
        user.username = name
        user.email = email
        user.is_active = is_active
        user.save()

    @override_settings(ACCOUNT_VERIFICATION_TIME=timedelta(seconds=1))
    def test_account_verification(self):
        active_user = self.create_user(name='active_user',
                                       email='active_user@email.com')
        inactive_user = self.create_user(name='inactive_user',
                                         email='inactive@email.com',
                                         is_active=False)
        sleep(3)
        account_verification()
        self.assertEquals(1, User.objects.all().count())
        self.assertEquals(0, User.objects.filter(is_active=False).count())
