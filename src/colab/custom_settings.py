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
    'south',
    'cliauth',

    # Own apps
    'super_archives',
    'api',
    'rss',
    'colab.deprecated',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
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

SOCKS_SERVER = None
SOCKS_PORT = None

try:
    from local_settings import *
except ImportError:
    pass
