"""
Test Form class.
Objective: Test parameters, and behavior.
"""

import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from colab.accounts.forms import UserCreationForm, UserChangeForm
from colab.accounts.models import User


class FormTest(TestCase):

    def setUp(self):
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

    def create_form_data(self, email, username):
        form_data = {'email': email,
                     'first_name': 'colabName',
                     'last_name': 'secondName',
                     'username': username,
                     'password1': '123colab4',
                     'password2': '123colab4'}
        form = UserCreationForm(data=form_data)
        return form

    def create_change_form_data(self, username):
        updated_data = {'username': username,
                        'email': 'email@email.com',
                        'last_login': datetime.date.today(),
                        'date_joined': datetime.date.today()}
        initial = {'email': 'email@email.com',
                   'first_name': 'colabName',
                   'last_name': 'secondName',
                   'username': 'colab',
                   'password': '123colab4'}
        form = UserChangeForm(initial=initial, data=updated_data)
        return form

    def test_already_registered_email(self):
        form = self.create_form_data('usertest@colab.com.br',
                                     'colab')
        self.assertFalse(form.is_valid())

    def test_registered_email_message(self):
        form = self.create_form_data('usertest@colab.com.br',
                                     'colab')
        msg = form.error_messages.get('duplicate_email') % {
            'url': reverse('login')
        }
        self.assertIn(msg, str(form))

    def test_valid_username(self):
        form = self.create_form_data('user@email.com',
                                     'colab123@colab-spb.com')
        self.assertTrue(form.is_valid())

    def test_not_valid_username(self):
        form = self.create_form_data('user@email.com',
                                     'colab!')
        self.assertFalse(form.is_valid())

    def test_update_valid_username(self):
        form = self.create_change_form_data('colab123@colab-spb.com')
        self.assertTrue(form.is_valid())

    def test_update_not_valid_username(self):
        form = self.create_change_form_data('colab!')
        self.assertFalse(form.is_valid())

    def tearDown(self):
        pass
