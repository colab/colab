# -*- coding:utf-8 -*-
from mock import patch

from django.test import TestCase, Client


class ArchivesViewTest(TestCase):

    fixtures = ['mailinglistdata.json']

    def setUp(self):
        self.client = Client()

    def authenticate_user(self):
        self.client.login(username='johndoe', password='1234')

    @patch('colab.super_archives.views.mailman.get_user_mailinglists',
           return_value=[{'listname': 'privatelist'}])
    @patch('colab.super_archives.views.mailman.list_users',
           return_value=['johndoe@example.com'])
    def test_see_only_private_list_if_member(self, mocklist, mockemail):
        self.authenticate_user()
        request = self.client.get('/archives/thread/')

        list_data = request.context['lists']

        self.assertEqual('lista', list_data[0].name)
        self.assertEqual('privatelist', list_data[1].name)
        self.assertEqual(2, len(list_data))

    def test_see_only_public_if_not_logged_in(self):
        request = self.client.get('/archives/thread/')

        list_data = request.context['lists']

        self.assertEqual('lista', list_data[0].name)
        self.assertEqual(1, len(list_data))

    @patch('colab.super_archives.views.mailman.get_user_mailinglists',
           return_value=[{'listname': 'privatelist'}])
    def test_see_private_thread_in_dashboard_if_member(self, mocklist):
        self.authenticate_user()
        request = self.client.get('/dashboard')

        latest_threads = request.context['latest_threads']
        hottest_threads = request.context['hottest_threads']

        self.assertEqual(4, len(latest_threads))
        self.assertEqual(4, len(hottest_threads))

    def test_dont_see_private_thread_if_logged_out(self):
        request = self.client.get('/dashboard')

        latest_threads = request.context['latest_threads']
        hottest_threads = request.context['hottest_threads']

        self.assertEqual(1, len(latest_threads))
        self.assertEqual(1, len(hottest_threads))

    def test_dont_see_private_threads_in_profile_if_logged_out(self):
        request = self.client.get('/account/johndoe')

        emails = request.context['emails']

        self.assertEqual(1, len(emails))
