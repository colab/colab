import sys

from django.test import TestCase, override_settings, Client
from django.conf import settings

from ..conf import (DatabaseUndefined, validate_database,
                    InaccessibleSettings, _load_py_file, load_py_settings,
                    load_colab_apps, load_widgets_settings)

from mock import patch


test_files_dir = "./colab/utils/tests"


class TestConf(TestCase):

    @override_settings(DEBUG=False, DATABASES={
        'default': {
            'NAME': settings.DEFAULT_DATABASE,
        },
    })
    def test_database_undefined(self):
        with self.assertRaises(DatabaseUndefined):
            validate_database(settings.DATABASES, settings.DEFAULT_DATABASE,
                              settings.DEBUG)

    def test_load_py_file_with_io_error(self):
        self.assertRaises(InaccessibleSettings,
                          _load_py_file, 'settings_test', '/etc/colab/')

    def test_load_py_file_with_syntax_error(self):
        with file('/tmp/settings_with_syntax_error.py', 'w') as temp_settings:
            temp_settings.write('(')

        self.assertRaises(InaccessibleSettings,
                          _load_py_file, 'settings_with_syntax_error', '/tmp')

    def test_load_py_file(self):
        py_settings = _load_py_file('colab_settings', test_files_dir)

        self.assertIn('SOCIAL_NETWORK_ENABLED', py_settings)
        self.assertTrue(py_settings['SOCIAL_NETWORK_ENABLED'])

        self.assertIn('EMAIL_PORT', py_settings)
        self.assertEquals(py_settings['EMAIL_PORT'], 25)

    @patch('os.getenv', return_value='/path/fake/settings.py')
    def test_load_py_settings_with_inaccessible_settings(self, mock):
        self.assertRaises(InaccessibleSettings, load_py_settings)

    @patch('os.getenv', return_value=test_files_dir + '/colab_settings.py')
    def test_load_py_settings_without_settings_d(self, mock):
        py_settings = load_py_settings('/path/fake/settings.d/test.py')

        self.assertIn('SOCIAL_NETWORK_ENABLED', py_settings)
        self.assertTrue(py_settings['SOCIAL_NETWORK_ENABLED'])

        self.assertIn('EMAIL_PORT', py_settings)
        self.assertEquals(py_settings['EMAIL_PORT'], 25)

    @patch('os.listdir', return_value=[test_files_dir + '/settings.d/test.py',
                                       'non_python_file'])
    @patch('colab.utils.conf._load_py_file',
           side_effect=[{'SOCIAL_NETWORK_ENABLED': True, 'EMAIL_PORT': 25},
                        {'TEST': 'test'}])
    def test_load_py_settings_with_settings_d(self, mock_py, mock_listdir):
        py_settings = load_py_settings(test_files_dir + '/settings.d/')

        self.assertIn('SOCIAL_NETWORK_ENABLED', py_settings)
        self.assertTrue(py_settings['SOCIAL_NETWORK_ENABLED'])

        self.assertIn('EMAIL_PORT', py_settings)
        self.assertEquals(py_settings['EMAIL_PORT'], 25)

        self.assertIn('TEST', py_settings)
        self.assertEquals(py_settings['TEST'], 'test')

    @patch('os.getenv', return_value='/path/fake/plugins.d/')
    def test_load_colab_apps_without_plugins_d_directory(self, mock):
        colab_apps = load_colab_apps()
        self.assertIn('COLAB_APPS', colab_apps)
        self.assertEquals(colab_apps['COLAB_APPS'], {})

    @patch('os.getenv', return_value=test_files_dir + '/plugins.d/')
    def test_load_colab_apps_with_plugins_d_directory(self, os_getenv):
        sys.path.insert(0, os_getenv.return_value)
        colab_apps = load_colab_apps()

        self.assertIn('gitlab', colab_apps['COLAB_APPS'])
        self.assertIn('noosfero', colab_apps['COLAB_APPS'])
        sys.path.remove(os_getenv.return_value)

        self.assertNotIn(os_getenv.return_value, sys.path)

    @patch('os.getenv', return_value='/path/fake/widgets_settings.py')
    def test_load_widgets_settings_without_settings(self, mock):
        self.assertIsNone(load_widgets_settings())

    @patch('os.getenv', side_effect=[test_files_dir + '/colab_settings.py',
                                     '/path/fake/widgets_settings.py'])
    def test_load_widgets_settings_without_settings_d(self, mock):
        self.assertIsNone(load_widgets_settings())

    def test_blacklist(self):
        client = Client()
        response = client.get('/test_blacklist')
        self.assertEquals(403, response.status_code)
