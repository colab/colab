from mock import patch

from django.test import TestCase

from colab.management.commands.celery import Command


class CeleryCommandTest(TestCase):

    @patch.object(Command, 'validate')
    @patch('colab.management.commands.celery.base.execute_from_commandline')
    def test_run_from_argv(self, execute_from_commandline_mock, validate_mock):
        cmd = Command()
        cmd.requires_system_checks = True

        cmd.run_from_argv(["arg1", "arg2", "arg3"])

        self.assertTrue(validate_mock.called)
        self.assertTrue(execute_from_commandline_mock.called)
