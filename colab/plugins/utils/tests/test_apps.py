from mock import patch

from django.test import TestCase
from django.apps import AppConfig

from colab.plugins.utils.apps import ColabPluginAppConfig


class AppsTest(TestCase):

    @patch.object(AppConfig, '_path_from_module')
    @patch('colab.plugins.utils.apps.get_plugin_config')
    def test_set_namespace(self, get_plugin_config_mock,
                           path_from_module_mock):
        path_from_module_mock.return_value = "/fake/path"

        get_plugin_config_mock.return_value = {'urls': {}}
        conf = get_plugin_config_mock()

        ColabPluginAppConfig("test", "test_app")

        self.assertIn('namespace', conf['urls'])
        self.assertEquals(None, conf['urls']['namespace'])
