"""
Test Form class.
Objective: Test parameters, and behavior.
"""

import datetime
from mock import patch

from django.test import TestCase
from django.core.urlresolvers import reverse

from colab.accounts.forms import UserCreationForm, UserChangeForm,\
    UserUpdateForm, UserForm, get_lists_choices
from colab.accounts import forms as accounts_forms
from colab.accounts.models import User
from colab.accounts.utils import mailman


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

    def tearDown(self):
        pass

    def create_form_data(self, email, username):
        form_data = {'email': email,
                     'first_name': 'colabName',
                     'last_name': 'secondName',
                     'username': username,
                     'password1': '123colab4',
                     'password2': '123colab4'}
        form = UserCreationForm(data=form_data)
        return form

    def create_update_form_data(self):
        updated_data = {'username': "colab",
                        'email': 'email@email.com',
                        'last_login': datetime.date.today(),
                        'date_joined': datetime.date.today(),
                        'twitter': 'nick_twitter',
                        'first_name': 'colabName',
                        'last_name': 'secondName',
                        }
        initial = {'email': 'email@email.com',
                   'first_name': 'colabName',
                   'last_name': 'secondName',
                   'username': 'colab',
                   'password': '123colab4'}
        form = UserUpdateForm(initial=initial, data=updated_data)
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

    def create_user_form_data(self):
        initial = {'email': 'email@email.com',
                   'first_name': 'colabName',
                   'last_name': 'secondName',
                   'username': 'colab',
                   'password': '123colab4'}
        form = UserForm(data=initial)
        return form

    def test_already_registered_email(self):
        form = self.create_form_data('usertest@colab.com.br',
                                     'colab')
        self.assertFalse(form.is_valid())
        self.assertIn('duplicate_email', form.error_messages)

    def test_registered_email_message(self):
        form = self.create_form_data('usertest@colab.com.br',
                                     'colab')
        msg = form.error_messages.get('duplicate_email') % {
            'url': reverse('login')
        }
        self.assertIn(msg, str(form))

    def test_valid_username(self):
        form = self.create_form_data('user@email.com',
                                     'colab123')
        self.assertTrue(form.is_valid())

    def test_already_created_username(self):
        form = self.create_form_data('usertest@colab.com.br',
                                     'USERtestCoLaB')
        self.assertFalse(form.is_valid())
        self.assertIn('duplicate_username', form.error_messages)

    def test_not_valid_username(self):
        form = self.create_form_data('user@email.com',
                                     'colab!')
        self.assertFalse(form.is_valid())

    def test_update_valid_username(self):
        form = self.create_change_form_data('colab123')
        self.assertTrue(form.is_valid())

    def test_update_not_valid_username(self):
        form = self.create_change_form_data('colab!')
        self.assertFalse(form.is_valid())

    @patch.object(accounts_forms, "validate_social_account")
    def test_validate_social_account(self, validate_social_account):
        validate_social_account.return_value = False

        form = self.create_update_form_data()
        self.assertFalse(form.is_valid())
        self.assertIn("Social account does not exist", form.errors['twitter'])

    def test_required_valid_fields_user_form(self):
        form_data = {
            'first_name': 'colabName',
            'last_name': 'secondName',
            'username': 'colab',
        }

        form = UserForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_required_empty_fields_user_form(self):
        form_data = {
            'first_name': '',
            'last_name': '',
            'username': '',
        }

        form = UserForm(data=form_data)

        self.assertFalse(form.is_valid())

        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('username', form.errors)

    def test_blank_required_fields_user_form(self):
        form_data = {
            'first_name': '  ',
            'last_name': '  ',
            'username': '  ',
        }

        form = UserForm(data=form_data)

        self.assertFalse(form.is_valid())

        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('username', form.errors)

    @patch.object(mailman, "all_lists")
    def test_get_list_choices(self, all_lists):
        all_lists.return_value = [
            {'listname': 'listA', 'description': 'A'},
            {'listname': 'listB', 'description': 'B'},
            {'listname': 'listC', 'description': 'C'},
            {'listname': 'listD', 'description': 'D'},
        ]
        lists = get_lists_choices()
        self.assertEqual(lists, [('listA', u'listA (A)'),
                                 ('listB', u'listB (B)'),
                                 ('listC', u'listC (C)'),
                                 ('listD', u'listD (D)')])
