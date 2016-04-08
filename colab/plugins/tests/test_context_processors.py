from django.test import TestCase, override_settings
from django.http import HttpRequest
from colab.plugins import context_processors


class ContextProcessorTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()

    @override_settings(COLAB_APPS={'plugin': 'plugin-data'})
    def test_colab_apps(self):
        response = context_processors.colab_apps(self.request)
        self.assertEqual({'plugins': {'plugin': 'plugin-data'}}, response)

    @override_settings(COLAB_APPS={'plugin':
                                   {'urls': {'prefix': '^plugin/'},
                                    'change_header': True}})
    def test_get_prefixes_change_header(self):
        prefixes = context_processors.get_prefixes()
        self.assertEqual(['^plugin/'], prefixes)

    @override_settings(COLAB_APPS={'plugin': {'urls': {'prefix': '^plugin/'}}})
    def test_get_prefixes_maintain_header(self):
        prefixes = context_processors.get_prefixes()
        self.assertEqual([], prefixes)

    @override_settings(COLAB_APPS={'plugin':
                                   {'urls': {'prefix': '^plugin/'},
                                    'change_header': True}})
    def test_change_header(self):
        self.request.path = '/plugin/'
        response = context_processors.change_header(self.request)
        self.assertEqual({'change_header': True}, response)

    @override_settings(COLAB_APPS={'plugin':
                                   {'urls': {'prefix': '^plugin/'},
                                    'change_header': True}})
    def test_change_header_other_url(self):
        self.request.path = '/otherurl/'
        response = context_processors.change_header(self.request)
        self.assertEqual({'change_header': False}, response)

    @override_settings(COLAB_APPS={'plugin':
                                   {'urls': {'prefix': '^plugin/'},
                                    'change_header': False}})
    def test_change_header_false(self):
        self.request.path = '/plugin/'
        response = context_processors.change_header(self.request)
        self.assertEqual({'change_header': False}, response)
