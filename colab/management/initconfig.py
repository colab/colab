
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


## Gitlab plugin - Put this in plugins.d/gitlab.py to actiate ##
# from django.utils.translation import ugettext_lazy as _
# from colab.plugins.utils.menu import colab_url_factory
#
# name = 'colab.plugins.gitlab'
# verbose_name = 'Gitlab Proxy'
#
# upstream = 'localhost'
# #middlewares = []
#
# urls = {{
#     'include': 'colab.plugins.gitlab.urls',
#     'namespace': 'gitlab',
#     'prefix': 'gitlab',
# }}
#
# menu_title = _('Code')
#
# url = colab_url_factory('gitlab')
#
# menu_urls = (
#     url(display=_('Public Projects'), viewname='gitlab',
#         kwargs={{'path': '/public/projects'}}, auth=False),
#     url(display=_('Profile'), viewname='gitlab',
#         kwargs={{'path': '/profile'}}, auth=True),
#     url(display=_('New Project'), viewname='gitlab',
#         kwargs={{'path': '/projects/new'}}, auth=True),
#     url(display=_('Projects'), viewname='gitlab',
#         kwargs={{'path': '/dashboard/projects'}}, auth=True),
#     url(display=_('Groups'), viewname='gitlab',
#         kwargs={{'path': '/profile/groups'}}, auth=True),
#     url(display=_('Issues'), viewname='gitlab',
#         kwargs={{'path': '/dashboard/issues'}}, auth=True),
#     url(display=_('Merge Requests'), viewname='gitlab',
#         kwargs={{'path': '/merge_requests'}}, auth=True),
#
# )
"""


def initconfig():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(50, chars)
    print(CONFIG_TEMPLATE.format(secret_key=secret_key))
