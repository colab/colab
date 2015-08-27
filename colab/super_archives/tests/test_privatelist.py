# -*- coding:utf-8 -*-
import mock

from colab.accounts.utils import mailman
from django.test import TestCase, Client


class ArchivesViewTest(TestCase):

    fixtures = ['mailinglistdata.json']

    def setUp(self):
        self.client = Client()

    def authenticate_user(self):
        self.client.login(username='johndoe', password='1234')

    def test_see_only_private_list_if_member(self):
        mailman.get_user_mailinglists = mock.Mock(
            return_value="[{'listname': 'privatelist'}]")
        mailman.extract_listname_from_list = mock.Mock(
            return_value="['privatelist']")
        mailman.list_users = mock.Mock(return_value="['johndoe@example.com']")

        self.authenticate_user()
        request = self.client.get('/archives/thread/')

        list_data = request.context['lists']

        self.assertEqual('lista', list_data[0][0])
        self.assertEqual('privatelist', list_data[1][0])
        self.assertEqual(2, len(list_data))

    def test_see_only_public_if_not_logged_in(self):
        request = self.client.get('/archives/thread/')

        list_data = request.context['lists']

        self.assertEqual('lista', list_data[0][0])
        self.assertEqual(1, len(list_data))

    def test_see_private_thread_in_dashboard_if_member(self):
        mailman.get_user_mailinglists = mock.Mock(
            return_value="[{'listname': 'privatelist'}]")
        mailman.extract_listname_from_list = mock.Mock(
            return_value="['privatelist']")

        self.authenticate_user()
        request = self.client.get('/dashboard')

        latest_threads = request.context['latest_threads']
        hottest_threads = request.context['hottest_threads']

        self.assertEqual(2, len(latest_threads))
        self.assertEqual(2, len(hottest_threads))

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
