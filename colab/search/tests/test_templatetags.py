# -*- coding:utf-8 -*-

from django.test import TestCase
from colab.search.templatetags.search_preview_templates import (
    get_search_preview_templates)
from mock import MagicMock, PropertyMock


class SearchTemplateTagsTest(TestCase):

    def setUp(self):
        self.model_indexed_mock = MagicMock()
        self.template_path = "{}/{}_search_preview.html"

    def set_mock_value(self, value):
        type(self.model_indexed_mock).type = PropertyMock(return_value=value)

    def test_get_search_preview_templates_with_user(self):
        self.set_mock_value("user")
        include_path = get_search_preview_templates(self.model_indexed_mock)
        self.assertEqual(include_path, self.template_path.format("search",
                                                                 "user"))

    def test_get_search_preview_templates_with_thread(self):
        self.set_mock_value("thread")
        include_path = get_search_preview_templates(self.model_indexed_mock)
        self.assertEqual(include_path,
                         self.template_path.format("search", "thread"))

    def test_get_search_preview_templates_with_plugin(self):
        self.set_mock_value("plugin_model")
        include_path = get_search_preview_templates(self.model_indexed_mock)
        self.assertEqual(include_path,
                         self.template_path.format("search", "plugin_model"))
