from mock import Mock

from django.test import TestCase

import colab.plugins.data.tasks
from colab.plugins.tasks import import_plugin_data


class TasksTest(TestCase):

    def test_import_plugin_data(self):
        task_mock = Mock(delay=Mock())

        colab.plugins.tasks.TASKS = [task_mock, task_mock, task_mock]

        import_plugin_data()
        self.assertEquals(3, task_mock.delay.call_count)

        colab.plugins.tasks.TASKS = []
