from mock import Mock
from django.test import TestCase, override_settings
from django.http import HttpRequest
from colab.accounts.models import User
from colab.middlewares.redirect_login import RedirectLoginMiddleware
from colab.middlewares.cookie_middleware import CookiePreHandlerMiddleware


class RedirectLoginTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.middleware = RedirectLoginMiddleware()

    def create_user(self):
        user = User()
        user.username = "USERtestCoLaB"
        user.set_password("123colab4")
        user.email = "usertest@colab.com.br"
        user.id = 1
        user.twitter = "usertestcolab"
        user.facebook = "usertestcolab"
        user.first_name = "USERtestCoLaB"
        user.last_name = "COLAB"
        user.save()

        return user

    def test_authenticated_user(self):
        user = self.create_user()
        self.request.user = user
        request = self.middleware.process_request(self.request)
        self.assertIsNone(request)

    def test_is_ajax(self):
        user = Mock()
        user.is_authenticated.return_value = False
        self.request.user = user
        self.request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        request = self.middleware.process_request(self.request)
        self.assertIsNone(request)

    def test_image_request(self):
        user = Mock()
        user.is_authenticated.return_value = False
        self.request.user = user
        self.request.META['HTTP_ACCEPT'] = 'image/webp,image/*,*/*;q=0.8'
        request = self.middleware.process_request(self.request)
        self.assertIsNone(request)

    @override_settings(COLAB_APPS_LOGIN_URLS=['/login/url'])
    def test_previous_path(self):
        user = Mock()
        user.is_authenticated.return_value = False
        self.request.user = user
        self.request.META['HTTP_ACCEPT'] = 'text/html; charset=utf-8'
        self.request.path = '/other/url'
        CookiePreHandlerMiddleware().process_request(self.request)
        self.middleware.process_request(self.request)
        self.assertEquals('/other/url',
                          self.request.COOKIES.get('_previous_path'))
