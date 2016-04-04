import unittest
from mock import patch

from colab.widgets.profile_widget import ProfileWidget
from django.http import HttpRequest, HttpResponse, StreamingHttpResponse

MOCK_APPS = {'mock_app': {
              'urls': {'prefix': '^mock_app'}
            }}


class WidgetProfileMock(ProfileWidget):
    app_name = 'mock_app'

    def __init__(self, content=""):
        self.content = content


@patch.dict('django.conf.settings.COLAB_APPS', MOCK_APPS)
class WidgetProfileTest(unittest.TestCase):

    def setUp(self):
        self.widget_prifile_mock = WidgetProfileMock()
        self.current_request = HttpRequest()
        self.response = HttpResponse()
        self.streaming_response = StreamingHttpResponse()

    def test_prefix(self):
        result = self.widget_prifile_mock.prefix
        self.assertEquals(result, '/mock_app')

    def test_default_url_exception(self):
        with self.assertRaises(NotImplementedError):
            self.widget_prifile_mock.default_url('request')

    def test_dispatch_exception(self):
        with self.assertRaises(NotImplementedError):
            self.widget_prifile_mock.dispatch('request', 'url')

    def test_fix_url(self):
        url = 'https://test:3000/mock_app/test'
        result = self.widget_prifile_mock.fix_url(url)
        self.assertEquals(result, '/test')

        url = 'https://test:3000/account/test'
        result = self.widget_prifile_mock.fix_url(url)
        self.assertEquals(result, url)

    def test_is_colab_form_with_colab_form(self):
        self.current_request.GET = {'path': '/'}
        self.current_request.POST = {'colab_form': 'true'}
        result = self.widget_prifile_mock.is_colab_form(self.current_request)
        self.assertTrue(result)

    def test_is_colab_form_without_colab_form(self):
        self.current_request.GET = {'path': '/'}
        self.current_request.POST = {}
        result = self.widget_prifile_mock.is_colab_form(self.current_request)
        self.assertFalse(result)

    def test_must_respond_without_path_in_request(self):
        self.current_request.GET = {}
        self.current_request.POST = {}
        result = self.widget_prifile_mock.must_respond(self.current_request)
        self.assertFalse(result)

    def test_must_respond_with_path_in_request(self):
        self.current_request.GET = {'path': '/test/mock_app/test_uri'}
        result = self.widget_prifile_mock.must_respond(self.current_request)
        self.assertTrue(result)

        self.current_request.GET = {}
        self.current_request.POST = {'path': '/test/mock_app/test_uri'}
        result = self.widget_prifile_mock.must_respond(self.current_request)
        self.assertTrue(result)

    def test_must_respond_with_colab_form_in_request(self):
        self.current_request.GET = {'path': '/mock_app/'}
        self.current_request.POST = {'path': '/mock_app/test',
                                     'colab_form': 'true'}
        result = self.widget_prifile_mock.must_respond(self.current_request)
        self.assertFalse(result)

    def test_change_request_method_without_post(self):
        self.current_request.POST = {}
        self.widget_prifile_mock.change_request_method(self.current_request)
        self.assertEquals(self.current_request.method, 'GET')

    def test_change_request_method_with_path(self):
        self.current_request.GET = {'path': '/mock_app/uri'}
        self.widget_prifile_mock.change_request_method(self.current_request)
        self.assertEquals(self.current_request.method, 'GET')

    def test_change_request_method_with_post(self):
        self.current_request.GET = {'path': '/mock_app/'}
        self.current_request.POST = {'path': '/'}
        self.widget_prifile_mock.change_request_method(self.current_request)
        self.assertEquals(self.current_request.method, 'POST')

    def test_change_request_method_with__method(self):
        self.current_request.POST = {'path': '/mock_app/uri_post',
                                     '_method': 'DELETE'}
        self.widget_prifile_mock.change_request_method(self.current_request)
        self.assertEquals(self.current_request.method, 'DELETE')

    @patch.object(WidgetProfileMock, 'default_url')
    def test_requested_url_without_path(self, default_url_mock):
        default_url = '/default/path'
        default_url_mock.return_value = default_url
        self.current_request.GET = {}
        self.current_request.POST = {}
        url = self.widget_prifile_mock.requested_url(self.current_request)
        self.assertEquals(url, default_url)

    @patch.object(WidgetProfileMock, 'default_url')
    def test_requested_url_with_path_and_no_colab_form(self, default_url_mock):
        default_url = '/default/path'
        path1 = '/mock_app/uri_1'
        path2 = '/mock_app/uri_2'
        default_url_mock.return_value = default_url

        self.current_request.GET = {'path': path1}
        self.current_request.POST = {}
        url = self.widget_prifile_mock.requested_url(self.current_request)
        self.assertEquals(url, '/uri_1')

        self.current_request.POST = {'path': path2}
        url = self.widget_prifile_mock.requested_url(self.current_request)
        self.assertEquals(url, '/uri_2')

    @patch.object(WidgetProfileMock, 'default_url')
    def test_requested_url_with_path_and_colab_form(self, default_url_mock):
        default_url = '/mock_app/default/path'
        path1 = '/mock_app/uri_1'
        path2 = '/mock_app/uri_2'
        default_url_mock.return_value = default_url
        self.current_request.GET = {'path': path1}
        self.current_request.POST = {'path': path2,
                                     'colab_form': 'true'}
        url = self.widget_prifile_mock.requested_url(self.current_request)
        self.assertEquals(url, '/default/path')

    @patch.object(WidgetProfileMock, 'dispatch')
    @patch.object(WidgetProfileMock, 'change_request_method')
    @patch.object(WidgetProfileMock, 'requested_url')
    def test_generate_content_with_content(self,
                                           requested_url_mock,
                                           change_request_method_mock,
                                           dispatch_mock):
        content = '<body>Content</body>'
        self.response.content = content
        dispatch_mock.return_value = self.response
        change_request_method_mock.return_value = None
        requested_url_mock.return_value = None

        self.widget_prifile_mock.generate_content(context={})
        self.assertEquals(self.widget_prifile_mock.content, content)

    @patch.object(WidgetProfileMock, 'dispatch')
    @patch.object(WidgetProfileMock, 'change_request_method')
    @patch.object(WidgetProfileMock, 'requested_url')
    def test_generate_content_with_streaming_content(
            self, requested_url_mock, change_request_method_mock,
            dispatch_mock):

        content = '<body>test streaming</body>'
        streaming_content = list(content)
        self.streaming_response.streaming_content = streaming_content
        dispatch_mock.return_value = self.streaming_response
        change_request_method_mock.return_value = None
        requested_url_mock.return_value = None

        self.widget_prifile_mock.generate_content(context={})
        self.assertEquals(self.widget_prifile_mock.content, content)
