from django.test import TestCase

from colab.widgets.widget_manager import WidgetManager, Widget

class WidgetManagerTest(TestCase):

    def test_add_widgets_to_key_area(self):
        area = 'profile'
        WidgetManager.register_widget(area, Widget())

        self.assertEqual(len(WidgetManager.get_widgets(area)), 1)

