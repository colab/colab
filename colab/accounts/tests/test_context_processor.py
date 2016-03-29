from mock import Mock
from django.test import TestCase, override_settings
from django.http import HttpRequest
from django.core.urlresolvers import reverse
from colab.accounts.context_processors import redirect_login
from colab.middlewares.redirect_login import RedirectLoginMiddleware
from colab.middlewares.cookie_middleware import CookiePreHandlerMiddleware


class ContextProcessorTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.middleware = RedirectLoginMiddleware()

    @override_settings(COLAB_APPS_LOGIN_URLS=['/login/url'])
    def test_redirect_login_previous_path(self):
        user = Mock()
        user.is_authenticated.return_value = False
        self.request.user = user
        self.request.META['HTTP_ACCEPT'] = 'text/html; charset=utf-8'
        self.request.path = '/other/url'
        CookiePreHandlerMiddleware().process_request(self.request)
        self.middleware.process_request(self.request)
        self.assertEquals({'previous_path': '/other/url'},
                          redirect_login(self.request))

    def test_redirect_login_home(self):
        user = Mock()
        user.is_authenticated.return_value = True
        self.request.user = user
        self.middleware.process_request(self.request)
        self.assertEquals({'previous_path': reverse('home')},
                          redirect_login(self.request))
