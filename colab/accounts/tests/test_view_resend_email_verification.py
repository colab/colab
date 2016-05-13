from mock import patch

from django.test import TestCase, Client
from colab.accounts.models import User
from colab.super_archives.models import (EmailAddress,
                                         EmailAddressValidation)


class TestResendEmailVerification(TestCase):

    def setUp(self):
        self.user = self.create_user_django()
        self.client = Client()

    def tearDown(self):
        self.user.delete()

    def create_user_django(self):
        user = User.objects.create_user("USERtestCoLaB",
                                        "usertest@colab.com.br", "123colab4")
        EmailAddress.objects.create(address=user.email, user=user)

        return user

    def test_get_request_in_resend_email_verification(self):
        response = self.client.get("/account/resend-email-verification/")
        self.assertEquals(200, response.status_code)

    def test_resend_email_verification_with_not_existing_email(self):
        options = {'email': 'nonexistent_email@gmail.com'}
        response = self.client.post("/account/resend-email-verification/",
                                    options)

        msg = 'This emails is not registered yet.'
        self.assertEquals(200, response.status_code)
        self.assertIn(msg, response.content)

    @patch.object(EmailAddressValidation, 'verify_email')
    def test_resend_email_verification_sending_email(self, verify_email_mock):
        verify_email_mock.return_value = True

        options = {'email': 'usertest@colab.com.br'}
        response = self.client.post("/account/resend-email-verification/",
                                    options)

        self.assertEquals(302, response.status_code)

        msg = 'An email was sent to you. Verify your message box.'
        response = self.client.get("/account/resend-email-verification/")
        self.assertEquals(200, response.status_code)
        self.assertIn(msg, response.content)

    @patch.object(EmailAddressValidation, 'verify_email')
    def test_resend_email_verification_not_sending_email(self,
                                                         verify_email_mock):
        verify_email_mock.return_value = False

        options = {'email': 'usertest@colab.com.br'}
        response = self.client.post("/account/resend-email-verification/",
                                    options)

        self.assertEquals(302, response.status_code)

        msg = 'An error occurred while sending mail.'
        response = self.client.get("/account/resend-email-verification/")
        self.assertEquals(200, response.status_code)
        self.assertIn(msg, response.content)
