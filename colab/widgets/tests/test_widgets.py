import unittest
from mock import patch

from colab.widgets.templatetags.widgets_tag import import_widgets
from colab.widgets.widget_manager import WidgetManager, Widget
from django.template import Context


class WidgetMock(Widget):

    def __init__(self, content=""):
        self.content = content


class WidgetsTest(unittest.TestCase):

    @patch.object(WidgetManager, 'get_widgets')
    def test_import_widgets_tag(self, get_widgets):
        return_list = [WidgetMock(), WidgetMock(), WidgetMock()]
        get_widgets.return_value = return_list

        context = Context({'request': ""})
        import_widgets(context, 'area')

        self.assertIn('widgets_area', context)
        self.assertEquals(context['widgets_area'], return_list)

    @patch.object(WidgetManager, 'get_widgets')
    def test_import_widgets_tag_with_named_var(self, get_widgets):
        return_list = [WidgetMock(), WidgetMock(), WidgetMock()]
        get_widgets.return_value = return_list

        context = Context({'request': ""})
        import_widgets(context, 'area', 'var')

        self.assertIn('var', context)
        self.assertEquals(context['var'], return_list)
