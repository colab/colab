"""
Test Signals class.
Objective: Test parameters, and behavior.
"""

from django.test import TestCase

from mock import patch, MagicMock, PropertyMock

from ..signals import registered_signals, register_signal, connect_signal, send
from ..exceptions import SignalDoesNotExist


class SignalsTest(TestCase):

    def setUp(self):
        self.list_signal = ['a', 'b', 'c']
        self.plugin_name = 'test_signal'

    def test_register_signal_(self):
        register_signal(self.plugin_name, self.list_signal)
        signal_name = 'a'
        signal_list = ['test_signal']
        self.assertEqual(len(registered_signals[signal_name]), 1)
        self.assertEqual(registered_signals[signal_name], signal_list)

    def test_register_signal_already_registered(self):
        signal_name = 'a'
        signal_list = ['test_signal']

        register_signal(self.plugin_name, self.list_signal)
        self.assertEqual(len(registered_signals[signal_name]), 1)

        register_signal(self.plugin_name, self.list_signal)
        self.assertEqual(len(registered_signals[signal_name]), 1)
        self.assertEqual(registered_signals[signal_name], signal_list)

    def test_connect_non_registered_signal(self):
        sender = 'Test'
        handling_method = 'Test'
        signal_name = 'Test'

        self.assertRaises(SignalDoesNotExist, connect_signal, signal_name,
                          sender, handling_method)

    @patch('colab.signals.signals.Signal.connect')
    def test_connect_already_registered_signal(self, mock):
        sender = 'Test'
        handling_method = MagicMock()
        type(handling_method).delay = PropertyMock(return_value='Test')
        signal_name = 'a'

        register_signal(self.plugin_name, self.list_signal)

        connect_signal(signal_name, sender, handling_method)
        args, kwargs = mock.call_args

        self.assertEqual(args[0], handling_method.delay)
        self.assertEqual(kwargs['sender'], sender)
        self.assertTrue(mock.is_called)

    @patch('colab.signals.signals.Signal.send')
    def test_send_signal(self, mock):
        sender = 'Test'
        signal_name = 'a'

        register_signal(self.plugin_name, self.list_signal)
        send(signal_name, sender)

        args, kwargs = mock.call_args

        self.assertEqual(kwargs['sender'], sender)
        self.assertTrue(mock.is_called)

    def test_send_signal_not_registered(self):
        self.assertRaises(SignalDoesNotExist, send, 'test_signal', 'test')
