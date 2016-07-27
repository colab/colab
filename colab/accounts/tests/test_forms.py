"""
Test Form class.
Objective: Test parameters, and behavior.
"""

import datetime
from django.test import TestCase, override_settings
from django.core.urlresolvers import reverse
from mock import patch
from colab.accounts import forms as accounts_forms
from colab.accounts.models import User
from colab.accounts.forms import (UserCreationForm, UserChangeForm,
                                  UserUpdateForm, UserForm,
                                  ColabSetPasswordForm,
                                  ColabPasswordChangeForm,
                                  ColabSetUsernameForm)


class SetPasswordFormTestCase(TestCase):

    TEST_COLAB_APPS = {
        'test_plugin': {
            'password_validators': (
                'colab.accounts.tests.utils.password_validator',
            )
        }
    }

    @property
    def user(self):
        return User.objects.create_user(username='test_user',
                                        email='test@example.com')

    @property
    def valid_form_data(self):
        return {'new_password1': '12345',
                'new_password2': '12345'}

    def test_no_custom_validators(self):
        form = ColabSetPasswordForm(self.user, data=self.valid_form_data)
        self.assertTrue(form.is_valid(), True)

    @override_settings(COLAB_APPS=TEST_COLAB_APPS)
    @patch('colab.accounts.tests.utils.password_validator')
    def test_custom_validator(self, validator):
        form = ColabSetPasswordForm(self.user, data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        validator.assert_called_with('12345')


class SetUsernameFormTestCase(TestCase):

    TEST_COLAB_APPS = {
        'test_plugin': {
            'username_validators': (
                'colab.accounts.tests.utils.username_validator',
            )
        }
    }

    @property
    def valid_form_data(self):
        return {'username': 'test_user',
                'email': 'test@email.com',
                'first_name': 'test',
                'last_name': 'test',
                'password1': '12345',
                'password2': '12345'}

    def test_no_custom_validators(self):
        form = ColabSetUsernameForm(data=self.valid_form_data)
        self.assertTrue(form.is_valid(), True)

    @override_settings(COLAB_APPS=TEST_COLAB_APPS)
    @patch('colab.accounts.tests.utils.username_validator')
    def test_custom_validator(self, validator):
        form = ColabSetUsernameForm(data=self.valid_form_data)

        self.assertTrue(form.is_valid())
        validator.assert_called_with('test_user')


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


class ChangePasswordFormTestCase(TestCase):

    TEST_COLAB_APPS = {
        'test_plugin': {
            'password_validators': (
                'colab.accounts.tests.utils.password_validator',
            )
        }
    }

    @property
    def user(self):
        u = User.objects.create_user(username='test_user',
                                     email='test@example.com')
        u.set_password("123colab4")
        return u

    @property
    def valid_form_data(self):
        return {'old_password': '123colab4',
                'new_password1': '12345',
                'new_password2': '12345'}

    def test_no_custom_validators(self):
        form = ColabPasswordChangeForm(self.user, data=self.valid_form_data)
        self.assertTrue(form.is_valid(), True)

    @override_settings(COLAB_APPS=TEST_COLAB_APPS)
    @patch('colab.accounts.tests.utils.password_validator')
    def test_custom_validator(self, validator):
        form = ColabPasswordChangeForm(self.user, data=self.valid_form_data)
        self.assertTrue(form.is_valid())
        validator.assert_called_with('12345')


class UserCreationFormTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='user1234',
                                            email='teste1234@example.com',
                                            first_name='test_first_name',
                                            last_name='test_last_name')

        cls.user.set_password("123colab4")
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def get_form_data(self, email, username='test_user',
                      password1='12345', password2='12345'):
        return {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2
        }

    def test_clean_mail_error(self):
        creation_form = UserCreationForm(
            data=self.get_form_data('teste1234@example.com'))
        self.assertFalse(creation_form.is_valid())
        self.assertTrue('email' in creation_form.errors)
        self.assertEqual(1, len(creation_form.errors))

    def test_clean_mail(self):
        creation_form = UserCreationForm(
            data=self.get_form_data('teste12345@example.com'))
        self.assertTrue(creation_form.is_valid())

    def test_clean_username_error(self):
        creation_form = UserCreationForm(
            data=self.get_form_data('teste12345@example.com',
                                    username='user1234'))
        self.assertFalse(creation_form.is_valid())
        self.assertTrue('username' in creation_form.errors)
        self.assertEqual(1, len(creation_form.errors))

    def test_clean_username(self):
        creation_form = UserCreationForm(
            data=self.get_form_data('teste12345@example.com',
                                    username='user12345'))
        self.assertTrue(creation_form.is_valid())

    def test_clean_password2_empty_password1(self):
        creation_form = UserCreationForm(
            data=self.get_form_data('teste12345@example.com',
                                    username='user12345',
                                    password1=''))
        self.assertFalse(creation_form.is_valid())
        self.assertTrue('password1' in creation_form.errors)
        self.assertEqual(1, len(creation_form.errors))

    def test_clean_password2_empty_password2(self):
        creation_form = UserCreationForm(
            data=self.get_form_data('teste12345@example.com',
                                    username='user12345',
                                    password2=''))
        self.assertFalse(creation_form.is_valid())
        self.assertTrue('password2' in creation_form.errors)

    def test_clean_password2_different_passwords(self):
        creation_form = UserCreationForm(
            data=self.get_form_data('teste12345@example.com',
                                    username='user12345',
                                    password1='1234'))
        self.assertFalse(creation_form.is_valid())
        self.assertTrue('password2' in creation_form.errors)
        self.assertEqual(1, len(creation_form.errors))
        self.assertEqual(1, len(creation_form.errors))

    def test_clean_password(self):
        creation_form = UserCreationForm(
            data=self.get_form_data('teste12345@example.com',
                                    username='user12345'))
        self.assertTrue(creation_form.is_valid())
