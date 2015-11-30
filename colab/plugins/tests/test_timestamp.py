import mock

from django.test import TestCase
from django.utils import timezone
from colab.plugins.models import TimeStampPlugin


class UserTest(TestCase):

    def test_update_timestamp_without_last_updated(self):
        result = timezone.datetime(2009, 1, 1).replace(tzinfo=timezone.utc)
        with mock.patch.object(timezone, 'datetime',
                               mock.Mock(wraps=timezone.datetime)) as mock_:
            mock_.now.return_value = result
            TimeStampPlugin.get_last_updated('TestPluginUpdate')
            TimeStampPlugin.update_timestamp('TestPluginUpdate')
            timestamp = TimeStampPlugin.get_last_updated('TestPluginUpdate')
        self.assertEquals(result, timestamp)

    def test_update_timestamp_with_last_updated(self):
        TimeStampPlugin.get_last_updated('TestPluginUpdate')
        date = '2015/12/23 00:00:00'
        TimeStampPlugin.update_timestamp('TestPluginUpdate', last_updated=date)

        timestamp = TimeStampPlugin.get_last_updated('TestPluginUpdate')
        result = timezone.datetime.strptime(date, "%Y/%m/%d %H:%M:%S")\
            .replace(tzinfo=timezone.utc)
        self.assertEquals(timestamp, result)

    def test_first_get_last_update(self):
        timestamp = TimeStampPlugin.get_last_updated('Test')
        self.assertEqual(timezone.datetime.min, timestamp)
