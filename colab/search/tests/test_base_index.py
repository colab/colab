# -*- coding:utf-8 -*-

import math
from mock import Mock

from django.test import TestCase,  Client
from colab.search.base_indexes import BaseIndex


class SearchViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_get_updated_field(self):
        base_index = BaseIndex()

        self.assertEquals('modified', base_index.get_updated_field())

    def test_get_boost(self):
        obj = Mock(hits=10)
        base_index = BaseIndex()

        self.assertEquals(1, base_index.get_boost(obj))

        obj = Mock(hits=11)
        self.assertEquals(math.log(11), base_index.get_boost(obj))

    def test_prepare_author(self):
        obj = Mock(author="author")
        base_index = BaseIndex()
        setattr(base_index, 'author_obj', None)

        self.assertEquals("author", base_index.prepare_author(obj))

        base_index.author_obj = Mock(username="carlin")
        self.assertEquals("carlin", base_index.prepare_author(obj))

    def test_prepare_author_url(self):
        base_index = BaseIndex()
        setattr(base_index, 'author_obj', None)

        self.assertEquals(None, base_index.prepare_author_url(None))

        base_index.author_obj = Mock(get_absolute_url=lambda: "url_test")
        self.assertEquals("url_test", base_index.prepare_author_url(None))

    class AuthorMockObject:
        author = "author"

    def test_prepare_modified_by(self):
        base_index = BaseIndex()
        setattr(base_index, 'author_obj', None)
        obj = self.AuthorMockObject()

        self.assertEquals("author", base_index.prepare_modified_by(obj))

        base_index.author_obj = Mock(get_full_name=lambda: "full_name")
        self.assertEquals("full_name", base_index.prepare_modified_by(obj))

        mock_modified_by = Mock(get_full_name=lambda: "full_name")
        obj = Mock(modified_by="somebody",
                   get_modified_by=lambda: mock_modified_by)

        self.assertEquals("full_name", base_index.prepare_modified_by(obj))

    def test_prepare_fullname_and_username(self):
        base_index = BaseIndex()
        setattr(base_index, 'author_obj', Mock(username="user",
                                               get_full_name=lambda: "name"))

        expected = "{}\n{}".format("name", "user")
        self.assertEquals(expected,
                          base_index.prepare_fullname_and_username(None))

        base_index.author_obj = None
        obj = self.AuthorMockObject()
        self.assertEquals("author",
                          base_index.prepare_fullname_and_username(obj))

        mock_modified_by = Mock(get_full_name=lambda: "full_name",
                                username="user")
        obj = Mock(modified_by="somebody",
                   get_modified_by=lambda: mock_modified_by)

        expected = "{}\n{}".format("full_name", "user")
        self.assertEquals(expected,
                          base_index.prepare_fullname_and_username(obj))

    def test_prepare_modified_by_url(self):
        base_index = BaseIndex()
        setattr(base_index, 'author_obj', None)

        self.assertEquals(None, base_index.prepare_modified_by_url(None))

        base_index.author_obj = Mock(get_absolute_url=lambda: "urlurl")
        self.assertEquals("urlurl", base_index.prepare_modified_by_url(None))

        mock_modified_by = Mock(get_absolute_url=lambda: "urlurl")
        obj = Mock(modified_by="somebody",
                   get_modified_by=lambda: mock_modified_by)

        self.assertEquals("urlurl", base_index.prepare_modified_by_url(obj))
