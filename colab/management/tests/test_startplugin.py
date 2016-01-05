import os
import os.path
import shutil
import string
import random

from django.test import TestCase
from django.core.management.base import CommandError

from colab.management.commands.startplugin import Command


class StartPluginCommandTest(TestCase):

    original_dir = '/tmp/app__test'
    options = {'files': [], 'settings': None, 'pythonpath': None,
               'verbosity': u'1', 'traceback': None, 'extensions': ['py'],
               'no_color': False, 'template': None}

    app_name = 'mock_app'
    app_name_dash = app_name.replace('_', '-')
    app_name_camel = app_name.title().replace('_', '')
    app_name_verbose = app_name.replace('_', ' ').title()

    def setUp(self):
        self.dir = self.original_dir

        # Creating a dir at tmp with a random salt
        while os.path.isdir(self.dir):
            random_salt = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for _ in range(4))
            self.dir += random_salt
        else:
            os.mkdir(self.dir)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_command(self):
        cmd = Command()
        cmd.handle(self.app_name, self.dir, **self.options)

    def test_empty_appname(self):
        cmd = Command()

        self.assertRaises(CommandError, cmd.handle, None, self.dir,
                          **self.options)
        self.assertRaises(CommandError, cmd.handle, "", self.dir,
                          **self.options)

    def test_valid_command(self):
        paths = ['setup.py',
                 'src',
                 'src/' + self.app_name,
                 'src/' + self.app_name + '/apps.py',
                 'src/' + self.app_name + '/data_importer.py',
                 'src/' + self.app_name + '/diazo.xml',
                 'src/' + self.app_name + '/__init__.py',
                 'src/' + self.app_name + '/models.py',
                 'src/' + self.app_name + '/search_indexes.py',
                 'src/' + self.app_name + '/urls.py',
                 'src/' + self.app_name + '/views.py',
                 'tests',
                 'tests/colab_settings.py',
                 'tests/__init__.py',
                 'tests/runtests.py',
                 'tests/test_plugin.py',
                 'tests/plugins.d',
                 'tests/plugins.d/' + self.app_name + '.py', ]

        self.run_command()

        for path in paths:
            dir = os.path.join(self.dir, path)
            self.assertTrue(os.path.exists(dir))

    def verify_presence_of(self, name, paths):
        self.run_command()

        for path in paths:
            dir = os.path.join(self.dir, path)
            self.assertTrue(os.path.exists(dir))

            with open(dir) as file:
                self.assertIn(name, ''.join(file.readlines()))

    def test_presence_of_app_name_verbose(self):
        paths = ["setup.py",
                 'src/' + self.app_name + '/apps.py',
                 'tests/plugins.d/' + self.app_name + '.py', ]
        self.verify_presence_of(self.app_name_verbose, paths)

    def test_presence_of_app_name_camel(self):
        paths = ['tests/test_plugin.py',
                 'src/' + self.app_name + '/views.py',
                 'src/' + self.app_name + '/apps.py',
                 'src/' + self.app_name + '/data_importer.py',
                 'src/' + self.app_name + '/urls.py', ]
        self.verify_presence_of(self.app_name_camel, paths)

    def test_presence_of_app_name_dash(self):
        paths = ["setup.py", ]
        self.verify_presence_of(self.app_name_dash, paths)

    def test_presence_of_app_name(self):
        paths = ['src/' + self.app_name + '/apps.py',
                 'src/' + self.app_name + '/data_importer.py',
                 'src/' + self.app_name + '/__init__.py',
                 'src/' + self.app_name + '/urls.py',
                 'src/' + self.app_name + '/views.py',
                 'tests/plugins.d/' + self.app_name + '.py', ]
        self.verify_presence_of(self.app_name, paths)
