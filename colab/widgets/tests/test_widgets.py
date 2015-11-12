import unittest
from mock import patch

from colab.widgets.templatetags.widgets_tag import import_widgets
from colab.widgets.widget_manager import WidgetManager


class WidgetsTest(unittest.TestCase):
    @patch.object(WidgetManager, 'get_widgets')
    def test_import_widgets_tag(self, get_widgets):
        return_list = [1, 2, 3]
        get_widgets.return_value = return_list

        context = {'request': ""}
        import_widgets(context, 'area')

        self.assertIn('widgets_area', context)
        self.assertEquals(context['widgets_area'], return_list)

    @patch.object(WidgetManager, 'get_widgets')
    def test_import_widgets_tag_with_named_var(self, get_widgets):
        return_list = [1, 2, 3]
        get_widgets.return_value = return_list

        context = {'request': ""}
        import_widgets(context, 'area', 'var')

        self.assertIn('var', context)
        self.assertEquals(context['var'], return_list)
