"""
Test Form class.
Objective: Test parameters, and behavior.
"""
from re import search

from django.test import TestCase

from colab.accounts.forms import UserForm
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

    def create_form_data(self):
        form_data = {'email': 'usertest@colab.com.br',
                     'first_name': 'colabName',
                     'last_name': 'secondName',
                     'username': 'colab',
                     'password1': '123colab4',
                     'password2': '123colab4'}
        form = UserForm(data=form_data)
        return form

    def test_already_registered_email(self):
        form = self.create_form_data()
        self.assertFalse(form.is_valid())

    def test_registered_email_message(self):
        tryToFind = r"<a href='login'>sign in<a/>"
        form = self.create_form_data()
        matched = search(tryToFind, str(form))
        self.assertIsNotNone(matched)

    def tearDown(self):
        pass
