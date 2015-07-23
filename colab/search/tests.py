# -*- coding:utf-8 -*-

from django.test import TestCase,  Client
from django.core.management import call_command


class SearchViewTest(TestCase):

    fixtures = ['test_data.json']

    def setUp(self):
        call_command('rebuild_index', interactive=False, verbosity=0)
        self.client = Client()

    def tearDown(self):
        call_command('clear_index', interactive=False, verbosity=0)

    def test_search_thread(self):
        request = self.client.get('/search/?q=thread')
        thread_list = request.context['page'].object_list

        self.assertEqual(3,  len(thread_list))

        condition = any('This is a repply to Thread 1 on list A' in
                        t.description for t in thread_list)
        self.assertTrue(condition)
        condition = any('This is a repply to Thread 1 on list B' in
                        t.description for t in thread_list)
        self.assertTrue(condition)
        condition = any('This is a repply to Thread 1 on list C' in
                        t.description for t in thread_list)
        self.assertTrue(condition)

    def test_search_account_by_firstName(self):
        request = self.client.get('/search/?q=Chuck')
        user_list = request.context['page'].object_list

        self.assertEqual(1, len(user_list))

        self.assertIn('chucknorris@mail.com',  user_list[0].object.email)
        self.assertIn('Chuck',  user_list[0].object.first_name)
        self.assertIn('Norris',  user_list[0].object.last_name)
        self.assertIn('chucknorris',  user_list[0].object.username)

    def test_search_account_by_lastName(self):
        request = self.client.get('/search/?q=Norris')
        user_list = request.context['page'].object_list

        self.assertEqual(2, len(user_list))

        self.assertIn('heisenberg@mail.com',  user_list[1].object.email)
        self.assertIn('Heisenberg',  user_list[1].object.first_name)
        self.assertIn('Norris',  user_list[1].object.last_name)
        self.assertIn('heisenbergnorris',  user_list[1].object.username)

        self.assertIn('chucknorris@mail.com',  user_list[0].object.email)
        self.assertIn('Chuck',  user_list[0].object.first_name)
        self.assertIn('Norris',  user_list[0].object.last_name)
        self.assertIn('chucknorris',  user_list[0].object.username)
