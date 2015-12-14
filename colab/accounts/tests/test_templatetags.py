from mock import Mock, patch

from django.test import TestCase

from colab.accounts.templatetags.date_format import (date_format,
                                                     datetime_format)


class TemplateTagsTest(TestCase):

    def test_date_format(self):
        date_mock = Mock(strftime=lambda x: "123", day="456", year="789")
        date_pattern = '%(m)s %(d)s %(y)s' % ({'m': '123', 'd': '456',
                                               'y': '789'})
        self.assertEquals(date_pattern, date_format(None, date_mock))

    @patch('colab.accounts.templatetags.date_format.date_format')
    def test_datetime_format(self, date_format_mock):
        date_format_mock.return_value = 'mock'
        date_mock = Mock(strftime=lambda x: "111", hour="000")

        time_pattern = '%(hour)s:%(min)s' % {'hour': "000", 'min': "111"}
        date_pattern = '%s at %s' % ("mock", time_pattern)

        self.assertEquals(date_pattern, datetime_format(None, date_mock))
