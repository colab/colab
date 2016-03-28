from django.test import TestCase

from colab.widgets.widget_manager import WidgetManager, Widget


class WigetMock(Widget):

    def __init__(self, content=""):
        self.content = content


class WidgetManagerTest(TestCase):

    html_content = "<head><meta charset='UTF-8'></head><body><p>T</p></body>"
    widget_area = 'profile'
    widget_id = 'widget_id'

    def overwritten_widget_instance(self, content=""):

        class WidgetOverwritten(Widget):
            identifier = 'widget_id'

            def generate_content(self, request=None):
                self.content = content
        return WidgetOverwritten()

    def default_widget_instance(self):

        class WidgetDefault(Widget):
            pass

        return WidgetDefault()

    def setUp(self):
        self.widget = self.overwritten_widget_instance(self.html_content)
        WidgetManager.register_widget(self.widget_area, self.widget)

    def tearDown(self):
        WidgetManager.unregister_widget(self.widget_area, self.widget_id)
        WidgetManager.bootstrap_conflict = False
        WidgetManager.jquery_conflict = False

    def test_widget_default_values(self):
        widget = self.default_widget_instance()
        self.assertEqual(widget.identifier, None)
        self.assertEqual(widget.name, None)
        self.assertEqual(widget.content, '')
        self.assertEqual(widget.template, '')

    def test_add_widgets_to_key_area(self):
        self.assertEqual(len(WidgetManager.get_widgets(self.widget_area)), 1)

    def test_remove_widgets_in_key_area(self):
        area = 'admin'
        widget_instance = self.overwritten_widget_instance(self.html_content)

        WidgetManager.register_widget(area, widget_instance)
        WidgetManager.unregister_widget(area, self.widget_id)

        self.assertEqual(len(WidgetManager.get_widgets(area)), 0)

    def test_get_body(self):
        self.widget = self.overwritten_widget_instance(self.html_content)

        self.widget.generate_content()
        self.assertEqual(self.widget.get_body(), "<p>T</p>")

    def test_get_header(self):
        self.widget = self.overwritten_widget_instance(self.html_content)

        self.widget.generate_content()
        self.assertEqual(self.widget.get_header(), "<meta charset='UTF-8'>")

    def test_get_header_wrong(self):
        widget = self.default_widget_instance()
        widget.content = "<head> Teste <head>"
        self.assertEqual(widget.get_header(), '')

    def test_get_without_body(self):
        widget = self.default_widget_instance()
        widget.content = "Teste"
        self.assertEqual(widget.get_body(), widget.content)

    def test_generate_content(self):
        widgets = WidgetManager.get_widgets(self.widget_area)
        self.assertEqual(widgets[0].content, self.html_content)

    def test_widget_with_invalid_area(self):
        self.assertEqual(WidgetManager.get_widgets("area"), [])

    def test_generate_content_without_template(self):
        widget = self.default_widget_instance()
        with self.assertRaises(Exception):
            widget.generate_content()

    def test_generate_content_with_template(self):
        widget = self.default_widget_instance()
        widget.template = self.html_content
        with self.assertRaises(Exception):
            widget.generate_content()

    def test_bootstrap_conflict(self):
        self.widget.bootstrap_conflict = True
        WidgetManager.get_widgets(self.widget_area)

        self.assertTrue(WidgetManager.bootstrap_conflict)
        self.assertFalse(WidgetManager.jquery_conflict)

    def test_jquery_conflict(self):
        self.widget.jquery_conflict = True
        WidgetManager.get_widgets(self.widget_area)

        self.assertTrue(WidgetManager.jquery_conflict)
        self.assertFalse(WidgetManager.bootstrap_conflict)
