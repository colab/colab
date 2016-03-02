from datetime import timedelta
from time import sleep

from colab.accounts.models import User
from colab.accounts.tasks import account_verification
from django.test import TestCase, override_settings


class TasksTest(TestCase):

    def create_user(self, name='samplename', email='test@email.com',
                    is_active=True):
        user = User()
        user.username = name
        user.email = email
        user.is_active = is_active
        user.save()

    @override_settings(ACCOUNT_VERIFICATION_TIME=timedelta(seconds=1))
    def test_account_verification(self):
        self.create_user(name='active_user', email='active_user@email.com')
        self.create_user(name='inactive_user', email='inactive@email.com',
                         is_active=False)
        sleep(5)
        account_verification()
        self.assertEqual(1, User.objects.count())
        self.assertEqual(0, User.objects.filter(is_active=False).count())
