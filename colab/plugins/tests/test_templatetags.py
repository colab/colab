from mock import Mock

from django.test import TestCase, Client
from django.core.cache import cache

from colab.plugins.templatetags import plugins
from colab.accounts.models import User


class PluginsMenuTest(TestCase):

    def setUp(self):
        self.user = self.create_user()
        self.client = Client()
        cache.clear()

    def tearDown(self):
        cache.clear()
        self.client.logout()

    def create_user(self):
        user = User()
        user.username = "USERtestCoLaB"
        user.set_password("123colab4")
        user.email = "usertest@colab.com.br"
        user.id = 1
        user.first_name = "USERtestCoLaB"
        user.last_name = "COLAB"
        user.save()

        return user

    def authenticate_user(self):
        self.client.login(username=self.user.username,
                          password="123colab4")

    def test_plugins_menu_without_menu_urls(self):
        self.authenticate_user()
        plugin_1 = {'menu_title': 'myTitle', 'menu_urls': []}

        test_context = {'user': self.user,
                        'plugins': {'plugin_1': plugin_1}}

        menu = plugins.plugins_menu(test_context)

        self.assertEquals(menu.strip(), "")

    def test_plugins_menu_with_1_menu_urls(self):
        self.authenticate_user()
        link = 'http://url'
        title = 'myTitle'
        plugin_1 = {'menu_title': title,
                    'menu_urls': [{'url': link, 'display': 'LRU'}]}

        test_context = {'user': self.user,
                        'plugins': {'plugin_1': plugin_1}}

        menu = plugins.plugins_menu(test_context)

        self.assertIn(link, menu)
        self.assertIn(title, menu)

    def test_plugins_menu_with_many_menu_urls(self):
        self.authenticate_user()

        link1 = 'http://url1'
        title1 = 'myTitle1'
        display1 = 'LRU1'
        link2 = 'http://url2'
        display2 = 'LRU2'

        plugin_1 = {'menu_title': title1,
                    'menu_urls': [{'url': link1, 'display': display1},
                                  {'url': link2, 'display': display2}]}

        test_context = {'user': self.user,
                        'plugins': {'plugin_1': plugin_1}}

        menu = plugins.plugins_menu(test_context)

        self.assertIn(link1, menu)
        self.assertIn(title1, menu)
        self.assertIn(display1, menu)
        self.assertIn(link2, menu)
        self.assertIn(display2, menu)

    def test_plugins_menu_with_multiple_plugins(self):
        self.authenticate_user()

        link1 = 'http://url1'
        title1 = 'myTitle1'
        display1 = 'LRU1'
        link2 = 'http://url2'
        display2 = 'LRU2'

        plugin_1 = {'menu_title': title1,
                    'menu_urls': [{'url': link1, 'display': display1},
                                  {'url': link2, 'display': display2}]}

        title2 = 'myTitle2'
        plugin_2 = {'menu_title': title2,
                    'menu_urls': []}

        test_context = {'user': self.user,
                        'plugins': {'plugin_1': plugin_1,
                                    'plugin_2': plugin_2}}

        menu = plugins.plugins_menu(test_context)

        self.assertIn(link1, menu)
        self.assertIn(title1, menu)
        self.assertIn(display1, menu)
        self.assertIn(link2, menu)
        self.assertIn(display2, menu)
        self.assertNotIn(title2, menu)

    class ColabUrlMock(Mock):
        def auth(self):
            return True

    def test_plugins_menu_with_inactivate_user(self):
        self.user.is_active = False
        self.user.save()

        self.authenticate_user()
        title = 'myTitle'
        plugin_1 = {'menu_title': title,
                    'menu_urls': [self.ColabUrlMock()]}

        test_context = {'user': self.user,
                        'plugins': {'plugin_1': plugin_1}}

        menu = plugins.plugins_menu(test_context)

        self.assertEquals("", menu.strip())
