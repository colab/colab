# -*- coding:utf-8 -*-

import mock

from colab.plugins.utils import filters_importer
from django.test import TestCase,  Client
from django.core.management import call_command
from colab.search.forms import ColabSearchForm


class SearchViewTest(TestCase):

    fixtures = ['test_data.json']

    def setUp(self):
        call_command('rebuild_index', interactive=False, verbosity=0)
        self.client = Client()

    def tearDown(self):
        call_command('clear_index', interactive=False, verbosity=0)

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

    def test_search_plugin_filters(self):
        plugin_filter = {
            'plugin_name': {
                'name': 'PluginData',
                'icon': 'plugin_icon',
                'fields': (
                    ('field_1', 'Field1', ''),
                    ('field_2', 'Field2', ''),
                ),
            },
        }
        filters_importer.import_plugin_filters = mock.Mock(
            return_value=plugin_filter)

        request = self.client.get('/search/?q=')

        value = [('plugin_name', 'PluginData', 'plugin_icon')]

        self.assertEqual(request.context['filters_options'], value)

    def test_search_dynamic_form_fields(self):
        plugin_filter = {
            'plugin_name': {
                'name': 'PluginData',
                'icon': 'plugin_icon',
                'fields': (
                    ('field_1', 'Field1', ''),
                    ('field_2', 'Field2', ''),
                ),
            },
        }
        filters_importer.import_plugin_filters = mock.Mock(
            return_value=plugin_filter)

        form = ColabSearchForm()

        self.assertIn('field_1', form.fields.keys())
        self.assertIn('field_2', form.fields.keys())

    def test_search_multiple_filters(self):
        request = self.client.get('/search/?q=&type=thread+user')
        user_list = request.context['page'].object_list

        self.assertEqual(3, len(user_list))

        self.assertIn('admin@mail.com',  user_list[0].object.email)
        self.assertIn('admin',  user_list[0].object.username)

        self.assertIn('chucknorris@mail.com',  user_list[1].object.email)
        self.assertIn('Chuck',  user_list[1].object.first_name)
        self.assertIn('Norris',  user_list[1].object.last_name)
        self.assertIn('chucknorris',  user_list[1].object.username)

        self.assertIn('heisenberg@mail.com',  user_list[2].object.email)
        self.assertIn('Heisenberg',  user_list[2].object.first_name)
        self.assertIn('Norris',  user_list[2].object.last_name)
        self.assertIn('heisenbergnorris',  user_list[2].object.username)
