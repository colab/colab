from django.test import TestCase
from django import http
from colab.middlewares.cookie_middleware import (StringMorsel,
                                                 CookiePostHandlerMiddleware,
                                                 CookiePreHandlerMiddleware,
                                                 CookieHandler)


class StringMorselTest(TestCase):

    def setUp(self):
        self.morsel = StringMorsel()
        self.morsel.set("cookie_name", "cookie_value", "coded_value")

    def test_string_morsel_str(self):
        self.assertEquals("cookie_value", self.morsel.__repr__())

    def test_string_morsel_eq(self):
        self.assertTrue(self.morsel == "cookie_value")
        other_morsel = StringMorsel()
        other_morsel.set("cookie_name", "cookie_value", "other_coded_value")
        self.assertFalse(other_morsel == self.morsel)
        self.assertFalse(other_morsel == 42)

    def test_string_morsel_ne(self):
        self.assertFalse(self.morsel != "cookie_value")
        other_morsel = StringMorsel()
        other_morsel.set("cookie_name", "cookie_value", "other_coded_value")
        self.assertTrue(other_morsel != self.morsel)
        self.assertTrue(other_morsel != 42)

    def test_string_morsel_split(self):
        self.assertIsInstance(self.morsel.split(), list)


class CookiePostHandlerTest(TestCase):

    def test_process_response(self):
        pre_handler = CookiePreHandlerMiddleware()
        post_handler = CookiePostHandlerMiddleware()

        request = http.HttpRequest()
        response = http.HttpResponse()

        pre_handler.process_request(request)
        request.COOKIES.set('cookie1', 'cookie_value1')
        request.COOKIES.set('cookie2', 'cookie_value2')

        response = post_handler.process_response(request, response)
        self.assertEquals(2, len(response.cookies))


class CookiePreHandlerTest(TestCase):

    def test_process_request(self):
        pre_handler = CookiePreHandlerMiddleware()
        request = http.HttpRequest()

        request.COOKIES['cookie1'] = 'cookie_value1'
        pre_handler.process_request(request)

        self.assertEquals('cookie_value1', request.COOKIES.get('cookie1'))


class CookieHandlerTest(TestCase):

    def setUp(self):
        self.cookie_handler = CookieHandler()

    def test_set(self):
        self.cookie_handler.set('key', 'value')
        self.assertEquals('value', self.cookie_handler.get('key'))
        self.cookie_handler.delete('key')
        self.assertEquals('', self.cookie_handler.get('key'))

    def test_set_with_domain(self):
        self.cookie_handler.set('key', 'value', domain="domain")
        self.assertEquals('value', self.cookie_handler.get('key'))
        self.cookie_handler.delete('key', domain="domain")
        self.assertEquals('', self.cookie_handler.get('key'))
