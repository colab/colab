from mock import Mock, patch

from django.test import TestCase
from colab.tz.middleware import TimezoneMiddleware


class TimezoneMiddlewareTest(TestCase):

    @patch('colab.tz.middleware.timezone.activate')
    def test_process_request_with_utc_offset(self, mock_timezone):
        mock_timezone.return_value = {}
        request = Mock(COOKIES={'utc_offset': 120})
        timezonemiddleware = TimezoneMiddleware()
        timezonemiddleware.process_request(request)
        self.assertTrue(mock_timezone.called)

    @patch('colab.tz.middleware.timezone.deactivate')
    def test_process_request_without_utc_offset(self, mock_timezone):
        mock_timezone.return_value = {}
        request = Mock(COOKIES={})
        timezonemiddleware = TimezoneMiddleware()
        timezonemiddleware.process_request(request)
        self.assertTrue(mock_timezone.called)

    @patch('colab.tz.middleware.pytz.FixedOffset')
    @patch('colab.tz.middleware.timezone.deactivate')
    def test_process_request_value_error(self, mock_timezone, mock_pytz):
        mock_pytz.side_effect = ValueError

        request = Mock(COOKIES={'utc_offset': 120})

        timezonemiddleware = TimezoneMiddleware()
        timezonemiddleware.process_request(request)
        self.assertTrue(mock_timezone.called)
