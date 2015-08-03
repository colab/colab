
from django.test import TestCase, override_settings
from django.conf import settings

from ..conf import DatabaseUndefined, validate_database


class TestConf(TestCase):

    @override_settings(DEBUG=False, DATABASES={
        'default': {
            'NAME': settings.DEFAULT_DATABASE,
        },
    })
    def test_database_undefined(self):
        with self.assertRaises(DatabaseUndefined):
            validate_database(settings.DATABASES, settings.DEFAULT_DATABASE,
                              settings.DEBUG)
