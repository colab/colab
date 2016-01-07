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
        date = '2015/12/23 00:00:00'
        self.create_sample_timestamp('TestPluginUpdate', date)
        timestamp = TimeStampPlugin.get_last_updated('TestPluginUpdate')
        self.assertEquals(self.create_timestamp_object(date), timestamp)

    def test_first_get_last_update(self):
        timestamp = TimeStampPlugin.get_last_updated('Test')
        self.assertEqual(timezone.datetime.min, timestamp)

    def create_sample_timestamp(self, class_name, date):
        TimeStampPlugin.get_last_updated(class_name)
        TimeStampPlugin.update_timestamp(class_name, last_updated=date)

    def create_timestamp_object(self, date):
        return timezone.datetime.strptime(date, "%Y/%m/%d %H:%M:%S")\
            .replace(tzinfo=timezone.utc)

    def test_verify_fields_of_timestamp_plugin(self):
        objects = [('TestPluginUpdate', '2015/12/23 00:00:00'),
                   ('NewPluginUpdate', '2015/09/10 00:00:00'),
                   ('OldPluginUpdate', '2014/10/01 00:00:00'),
                   ('ExamplePluginUpdate', '2013/11/03 00:00:00')]

        for object in objects:
            self.create_sample_timestamp(object[0], object[1])

        all_timestamps = TimeStampPlugin.objects.all()
        self.assertEqual(len(all_timestamps), 4)
        for object in objects:
            result = TimeStampPlugin.objects.filter(name=object[0])
            self.assertEqual(object[0], result[0].name)
            self.assertEqual(self.create_timestamp_object(object[1]),
                             result[0].timestamp)
