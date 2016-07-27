from django.test import TestCase, override_settings
from colab.plugins import helpers
from colab.plugins.exceptions import PluginDoesNotExistError


class HelpersTest(TestCase):

    @override_settings(COLAB_APPS={'plugin_name': {'plugin': 'infos'}})
    def test_get_plugin_config(self):
        self.assertEqual({'plugin': 'infos'},
                         helpers.get_plugin_config('plugin_name'))

    @override_settings(COLAB_APPS={'plugin_name': {'plugin': 'infos'}})
    def test_get_plugin_config_not_found(self):
        with self.assertRaises(PluginDoesNotExistError):
            helpers.get_plugin_config('invalid_name')

    @override_settings(COLAB_APPS={'plugin_name': {
                                   'urls': {'prefix': '^prefix/'}}})
    def test_get_plugin_prefix(self):
        self.assertEqual("^prefix/",
                         helpers.get_plugin_prefix('plugin_name'))

    @override_settings(COLAB_APPS={'plugin_name': {
                                   'urls': {'prefix': '^prefix/'}}})
    def test_get_plugin_prefix_no_regex(self):
        self.assertEqual("prefix/",
                         helpers.get_plugin_prefix('plugin_name', regex=False))
