
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


CONFIG_TEMPLATE = """
## Set to false in production
DEBUG = True
TEMPLATE_DEBUG = True

## System admins
ADMINS = [['John Foo', 'john@example.com'], ['Mary Bar', 'mary@example.com']]

MANAGERS = ADMINS

COLAB_FROM_ADDRESS = '"Colab" <noreply@example.com>'
SERVER_EMAIL = '"Colab" <noreply@example.com>'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = '[colab]'

SECRET_KEY = '{secret_key}'

ALLOWED_HOSTS = [
    'localhost',
#    'example.com',
#    'example.org',
#    'example.net',
]

### Uncomment to enable social networks fields profile
# SOCIAL_NETWORK_ENABLED = True

## Database settings
##
##     When DEBUG is True colab will create the DB on
##     the repository root. In case of production settings
##     (DEBUG False) the DB settings must be set.
##
# DATABASES = {{
#     'default': {{
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': '/path/to/colab.sqlite3',
#     }}
# }}

## Disable indexing
ROBOTS_NOINDEX = False

LOGGING = {{
    'version': 1,

    'handlers': {{
        'null': {{
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        }},
    }},

    'loggers': {{
        'colab.mailman': {{
            'handlers': ['null'],
            'propagate': False,
        }},
        'haystack': {{
            'handlers': ['null'],
            'propagate': False,
        }},
        'pysolr': {{
            'handlers': ['null'],
            'propagate': False,
        }},
    }},
}}
"""


class Command(BaseCommand):
    help = 'Returns an example config file for Colab'

    def handle(self, *args, **kwargs):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(50, chars)
        print(CONFIG_TEMPLATE.format(secret_key=secret_key))
