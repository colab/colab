from settings import *

DEBUG = False

TEMPLATE_DEBUG = False

TIME_ZONE = 'America/Sao_Paulo'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
    ('pt-br', gettext('Portuguese')),
)

LANGUAGE_CODE = 'pt-br'

INSTALLED_APPS = INSTALLED_APPS + (

    # Not standard apps
    'raven.contrib.django.raven_compat',
    'south',
    'cliauth',
    'django_browserid',

    # Own apps
    'super_archives',
    'api',
    'rss',
    'colab.deprecated',
    'planet',

    # Feedzilla and deps
    'feedzilla',
    'tagging',
    'common',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'sentry'],
            'level': 'ERROR',
            'propagate': True,
        },
       'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django_browserid': {
            'handlers': ['sentry', 'console'],
            'level': 'DEBUG',
        }
    }
}

SERVER_EMAIL = '"Colab Interlegis" <noreply@interlegis.leg.br>'
EMAIL_HOST_USER = SERVER_EMAIL

#SOLR_HOSTNAME = 'solr.interlegis.leg.br'
SOLR_HOSTNAME = '10.1.2.154'
SOLR_PORT = '8080'
SOLR_SELECT_PATH = '/solr/select'

SOLR_COLAB_URI = 'http://colab.interlegis.leg.br'
SOLR_BASE_QUERY = """
    ((Type:changeset OR Type:ticket OR Type:wiki OR Type:thread) AND Title:["" TO *])
"""

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django_browserid.context_processors.browserid',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Add the django_browserid authentication backend.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.auth.ColabBrowserIDBackend',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'colab', 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'www', 'static')

SOCKS_SERVER = None
SOCKS_PORT = None

from feedzilla.settings import *
FEEDZILLA_PAGE_SIZE = 5
FEEDZILLA_SITE_TITLE = gettext(u'Planet Colab')
FEEDZILLA_SITE_DESCRIPTION = gettext(u'Colab blog aggregator')

try:
    from local_settings import *
except ImportError:
    pass
