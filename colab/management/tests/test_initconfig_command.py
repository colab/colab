from StringIO import StringIO
from mock import patch

from django.test import TestCase

from colab.management.commands.initconfig import Command


class InitConfigCommandTest(TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_initconfig_command(self, stdout_mock):
        cmd = Command()
        cmd.handle()

        self.assertIn('DEBUG', stdout_mock.getvalue())
        self.assertIn('SECRET_KEY', stdout_mock.getvalue())
        self.assertIn('MANAGERS', stdout_mock.getvalue())
        self.assertIn('LOGGING', stdout_mock.getvalue())
        self.assertNotIn('AVOCADO', stdout_mock.getvalue())
