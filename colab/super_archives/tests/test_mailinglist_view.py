# -*- coding:utf-8 -*-

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from mock import patch


class MailingListViewTest(TestCase):

    fixtures = ['mailinglistviewdata.json', 'test_user.json']

    def setUp(self):
        self.client = Client()
        self.username = 'chucknorris'

    def authenticate_user(self):
        self.client.login(username=self.username, password='admin')

    def test_get_query_set_with_latest_order(self):
        response = self.client.get(
            '/archives/mailinglist/publiclist?order=latest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['thread_list']), 3)

        expected_order = ['Subject6', 'Subject5', 'Subject4']
        for i in range(3):
            self.assertEqual(
                'publiclist',
                response.context['thread_list'][i].mailinglist.name
            )
            self.assertEqual(
                expected_order[i],
                response.context['thread_list'][i].subject_token
            )

    def test_get_query_set_with_rating_order(self):
        response = self.client.get(
            '/archives/mailinglist/publiclist?order=rating'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['thread_list']), 3)

        expected_order = ['Subject4', 'Subject5', 'Subject6']
        for i in range(3):
            self.assertEqual(
                'publiclist',
                response.context['thread_list'][i].mailinglist.name
            )
            self.assertEqual(
                expected_order[i],
                response.context['thread_list'][i].subject_token
            )

    def test_get_context_data(self):
        response = self.client.get(
            '/archives/mailinglist/publiclist?order=rating'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual('publiclist', response.context['mailinglist'].name)
        self.assertEqual('rating', response.context['selected'])
        self.assertIn('rating', response.context['order_data'])
        self.assertIn('latest', response.context['order_data'])

    def test_private_list_access_with_user_not_logged_in(self):
        response = self.client.get(
            '/archives/mailinglist/privatelist',
            follow=True
        )

        expected_url = 'http://testserver/account/login'
        expected_message = 'You are not logged in'

        self.assertEqual(200, response.status_code)
        self.assertIn(expected_message, response.content)
        self.assertRedirects(response, expected_url)

    @patch('colab.super_archives.views.mailman.get_user_mailinglists',
           return_value=[{'listname': 'colabtest'}])
    def test_private_list_access_with_user_without_permission(self, mock):
        self.authenticate_user()
        response = self.client.get(
            '/archives/mailinglist/privatelist',
            follow=True
        )

        expected_url = 'http://testserver'
        expected_url += reverse('user_list_subscriptions',
                                kwargs={'username': self.username})

        self.assertEqual(200, response.status_code)
        self.assertRedirects(response, expected_url)

    @patch('colab.super_archives.views.mailman.get_user_mailinglists',
           return_value=[{'listname': 'privatelist'}])
    def test_private_list_access_with_user_permission(self, mock):
        self.authenticate_user()
        response = self.client.get(
            '/archives/mailinglist/privatelist'
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.context['thread_list']), 1)
        self.assertEqual(response.context['thread_list'][0].mailinglist.name,
                         'privatelist')
        self.assertEqual(response.context['thread_list'][0].subject_token,
                         'Subject3')
