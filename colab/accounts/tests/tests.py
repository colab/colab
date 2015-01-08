"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from colab.accounts.views import ManageUserSubscriptionsView
from colab.accounts.views import UserProfileDetailView
from colab.accounts.models import User
from django.http.response import Http404
from colab.accounts.views import signup

class AccountsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_successful_signup(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@doe.com',
            'username': 'johndoe',
        }

        post_request = self.factory.post('/account/register/', data=form_data)
        
        # It makes unittest understant it must add messages
        # See: https://code.djangoproject.com/ticket/17971
        setattr(post_request, 'session', 'session')
        messages = FallbackStorage(post_request)
        setattr(post_request, '_messages', messages)
        
        response = signup(post_request)
        
        self.assertEqual('/account/johndoe', response['Location'])


    def test_invalid_user_profile_url(self):            
        response = self.client.get('/account/johndoe/')
        self.assertEqual(404, response.status_code)

    def test_valid_user_profile_url(self):
        self.userTest = User()
        self.userTest.username = "usertest"
        self.userTest.email = "usertest@colab.com.br"
        self.userTest.set_password("1234colab")
        self.userTest.save()
        response = self.client.get('/account/usertest/')
        self.assertEqual(200, response.status_code)

