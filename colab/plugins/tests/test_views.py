from django.test import TestCase
from django.test.client import RequestFactory

from ..views import ColabProxyView
from colab.accounts.models import User


class ViewsTest(TestCase):

    def setUp(self):
        self.view = ColabProxyView()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='john', email='john@test.org', password='123',
            first_name='John', last_name='John')

    def test_dispatch_without_app_label(self):
        request = self.factory.get('/')
        request.user = self.user

        with self.assertRaises(NotImplementedError):
            self.view.dispatch(request, '/')
