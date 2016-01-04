"""
Test Mailman class.
Objective: Test parameters, and behavior.
"""
from mock import patch, Mock

from django.test import TestCase
from colab.accounts.utils import mailman


class TestMailman(TestCase):

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
        admin = Mock()
        admin.email = 'test@test.test'
        value = ('testlist', admin)
        method = 'create_list'
        result = self.request_mock(method, value, 0)
        self.assertTrue("success" in result)
        result = self.request_mock(method, value, '')
        self.assertFalse("success" in result)
