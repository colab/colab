from django.test import TestCase

from colab.widgets.widget_manager import WidgetManager, Widget


class WidgetManagerTest(TestCase):

    html_content = "<head><meta charset='UTF-8'></head><body><p>T</p></body>"
    widget_area = 'profile'
    widget_id = 'widget_id'

    def custom_widget_instance(self, content):

        class CustomWidget(Widget):
            identifier = 'widget_id'

            def generate_content(self, request=None):
                self.content = content
        return CustomWidget()

    def setUp(self):
        custom_widget = self.custom_widget_instance(self.html_content)
        WidgetManager.register_widget(self.widget_area, custom_widget)

    def tearDown(self):
        WidgetManager.unregister_widget(self.widget_area, self.widget_id)

    def test_add_widgets_to_key_area(self):
        self.assertEqual(len(WidgetManager.get_widgets(self.widget_area)), 1)

    def test_remove_widgets_in_key_area(self):
        area = 'admin'
        widget_instance = self.custom_widget_instance(self.html_content)

        WidgetManager.register_widget(area, widget_instance)
        WidgetManager.unregister_widget(area, self.widget_id)

        self.assertEqual(len(WidgetManager.get_widgets(area)), 0)

    def test_get_body(self):
        customWidget = self.custom_widget_instance(self.html_content)

        customWidget.generate_content()
        self.assertEqual(customWidget.get_body(), "<p>T</p>")

    def test_get_header(self):
        customWidget = self.custom_widget_instance(self.html_content)

        customWidget.generate_content()
        self.assertEqual(customWidget.get_header(), "<meta charset='UTF-8'>")

    def test_generate_content(self):
        widgets = WidgetManager.get_widgets(self.widget_area)
        self.assertEqual(widgets[0].content, self.html_content)
