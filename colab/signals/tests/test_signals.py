"""
Test Signals class.
Objective: Test parameters, and behavior.
"""

from django.test import TestCase
from colab.signals.signals import Signals
from mock import patch


class SignalsTest(TestCase):

    def setUp(self):
       self.list_signal = ['a', 'b', 'c']
       self.plugin_name = 'test_signal'
       self.signals = Signals()


    def test_register_signal_(self):
       self.signals.register_signal(self.plugin_name, self.list_signal)

       signal_name ='a'
       signal_list = ['test_signal']
       self.assertEqual(len(self.signals.registered_signals[signal_name]), 1)
       self.assertEqual(self.signals.registered_signals[signal_name],
               signal_list)

   
    def test_register_signal_already_registered(self):
       signal_name ='a'
       signal_list = ['test_signal']

       self.signals.register_signal(self.plugin_name, self.list_signal)
       self.assertEqual(len(self.signals.registered_signals[signal_name]), 1)

       self.signals.register_signal(self.plugin_name, self.list_signal)
       self.assertEqual(len(self.signals.registered_signals[signal_name]), 1)
       self.assertEqual(self.signals.registered_signals[signal_name],
               signal_list)

    
    def test_connect_non_registered_signal(self):
        sender = 'Test'
        handling_method = 'Test'
        signal_name = 'Test'
        
        self.assertRaises(Exception, self.signals.connect_signal, signal_name,
                sender, handling_method) 


    @patch('colab.signals.signals.Signal.connect')
    def test_connect_already_registered_signal(self, mock):
        sender = 'Test'
        handling_method = 'Test'
        signal_name = 'a'
        
        self.signals.register_signal(self.plugin_name, self.list_signal)

        self.signals.connect_signal(signal_name, sender, handling_method)
        args, kwargs = mock.call_args
        
        self.assertEqual(args[0], handling_method)
        self.assertEqual(kwargs['sender'], sender)
        self.assertTrue(mock.is_called)
        

    @patch('colab.signals.signals.Signal.send')
    def test_send_signal(self, mock):
        sender = 'Test'
        handling_method = 'Test'
        signal_name = 'a'
        
        self.signals.register_signal(self.plugin_name, self.list_signal)
        self.signals.send(signal_name, sender)

        args, kwargs = mock.call_args

        self.assertEqual(kwargs['sender'], sender)
        self.assertTrue(mock.is_called)
        


