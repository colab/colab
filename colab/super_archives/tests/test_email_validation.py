# -*- coding:utf-8 -*-

from mock import patch

from colab.accounts.models import User
from django.test import TestCase, Client
from colab.super_archives.models import EmailAddressValidation, EmailAddress


class EmailValidationTest(TestCase):

    fixtures = ['test_user.json']

    def setUp(self):
        self.client = Client()

    def authenticate_user(self):
        self.client.login(username='chucknorris', password='123colab4')

    @patch('colab.super_archives.views.send_verification_email',
           return_value="")
    def test_send_verification_email_successfuly(self,
                                                 mock_send_verification_email):
        user = User.objects.get(username='chucknorris')

        EmailAddressValidation.create(user.email, user)

        email_addr, created = EmailAddress.objects.get_or_create(
            address=user.email)
        email_addr.user = user
        email_addr.save()

        self.authenticate_user()

        response = self.client.post('/archives/manage/email/validate/',
                                    {'user': user.id, 'email': user.email})

        self.assertEqual(response.status_code, 204)
        self.assertTrue(mock_send_verification_email.called)

    @patch('colab.super_archives.views.send_verification_email',
           return_value="")
    def test_send_verification_email_with_not_verified_email(
            self, send_verification_email):
        self.authenticate_user()

        user = User.objects.get(username='chucknorris')

        response = self.client.post('/archives/manage/email/validate/',
                                    {
                                        'user': user.id,
                                        'email': "email@mail.com",
                                    })

        self.assertEqual(response.status_code, 404)
        self.assertFalse(send_verification_email.called)

    @patch('colab.super_archives.views.send_verification_email',
           return_value="")
    def test_send_verification_email_with_not_valid_user_id(
            self, send_verification_email):
        self.authenticate_user()

        user = User.objects.get(username='chucknorris')

        response = self.client.post('/archives/manage/email/validate/',
                                    {'user': len(User.objects.all()) + 1,
                                     'email': user.email})

        self.assertEqual(response.status_code, 404)
        self.assertFalse(send_verification_email.called)
