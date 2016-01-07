# -*- coding:utf-8 -*-

from django.test import TestCase, Client


class MailingListViewTest(TestCase):

    fixtures = ['mailinglistdata.json', 'test_user.json']

    def setUp(self):
        self.client = Client()

    def authenticate_user(self):
        self.client.login(username='chucknorris', password='123colab4')

    def test_get_query_set_with_no_order(self):
        response = self.client.get('/archives/mailinglist/mailman')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['thread_list']), 1)
        self.assertEqual(response.context['thread_list'][0].mailinglist.name,
                         'mailman')
        self.assertEqual(response.context['thread_list'][0].subject_token,
                         'Subject1')

    def test_get_query_set_with_latest_order(self):
        response = self.client.get(
            '/archives/mailinglist/privatelist?order=latest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['thread_list']), 3)

        expected_order = ['Subject5', 'Subject4', 'Subject3']
        for i in range(3):
            self.assertEqual(
                'privatelist',
                response.context['thread_list'][i].mailinglist.name
            )
            self.assertEqual(
                expected_order[i],
                response.context['thread_list'][i].subject_token
            )

    def test_get_query_set_with_rating_order(self):
        response = self.client.get(
            '/archives/mailinglist/privatelist?order=rating'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['thread_list']), 3)

        expected_order = ['Subject3', 'Subject4', 'Subject5']
        for i in range(3):
            self.assertEqual(
                'privatelist',
                response.context['thread_list'][i].mailinglist.name
            )
            self.assertEqual(
                expected_order[i],
                response.context['thread_list'][i].subject_token
            )

    def test_get_context_data(self):
        response = self.client.get(
            '/archives/mailinglist/privatelist?order=rating'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual('privatelist', response.context['mailinglist'].name)
        self.assertEqual('rating', response.context['selected'])
        self.assertIn('rating', response.context['order_data'])
        self.assertIn('latest', response.context['order_data'])
