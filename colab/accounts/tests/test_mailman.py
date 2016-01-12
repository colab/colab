"""
Test Mailman class.
Objective: Test parameters, and behavior.
"""
from mock import patch, Mock

from django.test import TestCase
from colab.accounts.utils import mailman
from colab.accounts.models import User


class TestMailman(TestCase):

    def create_user(self):
        user = User()
        user.username = "usertest"
        user.set_password("123colab4")
        user.email = "usertest@colab.com.br"
        user.id = 1
        user.twitter = "usertest"
        user.facebook = "usertest"
        user.first_name = "usertest"
        user.last_name = "COLAB"
        user.save()

        return user

    @patch('colab.accounts.utils.mailman.requests')
    def request_mock(self, method, value, json_return, mock_requests):
        mock_response = Mock()
        mock_response.json.return_value = json_return
        mock_response.status_code = 201
        mock_requests.put.return_value = mock_response
        mock_requests.post.return_value = mock_response
        mock_requests.get.return_value = mock_response
        mock_requests.delete.return_value = mock_response
        self.mock_response = mock_response
        self.mock_requests = mock_requests
        return getattr(mailman, method)(*value)

    def test_subscribe(self):
        value = ('testlist', 'address')
        method = 'subscribe'
        result = self.request_mock(method, value, 0)
        self.assertTrue("success" in result)
        result = self.request_mock(method, value, '')
        self.assertFalse("success" in result)

    def test_unsubscribe(self):
        value = ('testlist', 'address')
        method = 'unsubscribe'
        result = self.request_mock(method, value, 0)
        self.assertTrue("success" in result)
        result = self.request_mock(method, value, '')
        self.assertFalse("success" in result)

    def test_create_list(self):
        self.create_user()
        admin = Mock()
        admin.username = 'usertest'
        value = ('testlist', admin)
        method = 'create_list'
        result = self.request_mock(method, value, 0)
        self.assertIn("success", result)
        value = ('testlist2', admin)
        result = self.request_mock(method, value, '')
        self.assertNotIn("success", result)
