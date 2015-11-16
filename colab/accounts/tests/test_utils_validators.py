from django.test import TestCase

from ..utils.validators import validate_social_account


class TestValidators(TestCase):

    def test_validate_social_account_with_fake_account(self):
        self.assertFalse(validate_social_account('john-fake',
                                                 'http://twitter.com'))

    def test_validate_social_account(self):
        self.assertTrue(validate_social_account('john', 'http://twitter.com'))
