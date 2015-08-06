from django.test import TestCase
from mock import patch, MagicMock
from colab.plugins.utils import signals


class SignalsTest(TestCase):
    @patch("colab.plugins.utils.signals.apps.get_app_configs")
    def test_init_signals(self, mock_app):
        method_name = 'test'

        app_mock = MagicMock()

        apps_list = ['a', 'b', app_mock]

        mock_app.return_value = apps_list
        signals._init_signals(method_name)

        app_mock.test.assert_called_with()
        self.assertEqual(1, app_mock.test.call_count)
        self.assertTrue(app_mock.test.called)
