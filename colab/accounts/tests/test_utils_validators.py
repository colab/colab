import urllib2
from mock import patch, Mock

from django.test import TestCase

from ..utils.validators import validate_social_account


class TestValidators(TestCase):

    @patch('urllib2.urlopen',
           side_effect=urllib2.HTTPError(500, "test", 1, 2, None))
    def test_validate_social_account_with_fake_account(self, urlopen_mock):
        self.assertFalse(validate_social_account('john-fake',
                                                 'http://twitter.com'))

    @patch('urllib2.urlopen', return_value=Mock(code=200))
    def test_validate_social_account(self, urlopen_mock):
        self.assertTrue(validate_social_account('john', 'http://twitter.com'))
