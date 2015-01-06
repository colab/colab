"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
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


    def test_invalid_user(self):
     
        get_request = self.factory.get('/account/johndoe/')

	has404 = False;

	try:
            response = UserProfileDetailView.as_view()(get_request, username='johndoe')
	except Http404:
		has404 = True;

	self.assertTrue(has404)
