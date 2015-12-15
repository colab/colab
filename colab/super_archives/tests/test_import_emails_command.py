# -*- coding:utf-8 -*-

from mock import Mock, patch
from StringIO import StringIO

from django.test import TestCase
from django.core.management.base import OutputWrapper

from colab.super_archives.management.commands.import_emails import Command


class ImportEmailsCommandTest(TestCase):

    TEST_LOCK_FILE = "/tmp/lock_import_emails_test_files.lock"
    MAILINGLISTS_DIR = "tests/mailman_lists/"
    MAILINGLIST_FILE = ("tests/mailman_lists/mock_maillist.mbox/" +
                        "mock_maillist.mbox")

    def setUp(self):
        self.cmd = Command()
        self.cmd.stdout = OutputWrapper(StringIO())
        self.cmd.stderr = OutputWrapper(StringIO())
        self.cmd.lock_file = self.TEST_LOCK_FILE

    def test_log(self):
        msg = "Test out message"
        self.cmd.log(msg)

        self.assertIn(msg, self.cmd.stdout.getvalue().strip())

        msg_error = "Test error message"
        self.cmd.log(msg_error, True)

        self.assertIn(msg_error, self.cmd.stderr.getvalue().strip())

    def test_parse_emails(self):
        bodies = ""
        count_emails = 0
        for index, email in self.cmd.parse_emails(self.MAILINGLIST_FILE):
            bodies += email.get_body()
            count_emails += 1

        self.assertIn("mock test", bodies)
        self.assertNotIn("not in this test", bodies)
        self.assertEquals(2, count_emails)

    def test_get_all_emails(self):
        bodies = {}
        get_emails = self.cmd.get_emails(self.MAILINGLISTS_DIR, True,
                                         ['mock_maillist_again'])
        for name, email, index in get_emails:
            bodies[name] = email.get_body()

        self.assertIn('mock_maillist', bodies)
        self.assertIn('mock test', bodies['mock_maillist'])

        self.assertNotIn('mock_maillist_again', bodies)

    def test_get_emails_from_the_last_import_without_valid_list(self):
        bodies = {}
        get_emails = self.cmd.get_emails(self.MAILINGLISTS_DIR, False,
                                         ['mock_maillist_again'])
        for name, email, index in get_emails:
            bodies[name] = email.get_body()

        self.assertIn('mock_maillist', bodies)
        self.assertIn('mock test', bodies['mock_maillist'])

        self.assertNotIn('mock_maillist_again', bodies)

    @patch('colab.super_archives.management.commands.import_emails.' +
           'MailingList.objects.get')
    def test_get_emails_from_the_last_import_with_valid_list(self,
                                                             get_list_mock):
        get_list_mock.return_value = Mock(last_imported_index=1)

        bodies = {}
        msg_count = {}
        get_emails = self.cmd.get_emails(self.MAILINGLISTS_DIR, False,
                                         ['mock_maillist_again'])
        for name, email, index in get_emails:
            bodies[name] = email.get_body()
            if name not in msg_count:
                msg_count[name] = 1
            else:
                msg_count[name] += 1

        self.assertIn('mock_maillist', bodies)
        self.assertIn('mock test', bodies['mock_maillist'])

        self.assertIn('mock_maillist', msg_count)
        self.assertEquals(1, msg_count['mock_maillist'])

        self.assertNotIn('mock_maillist_again', bodies)
