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

DJANGO_DATE_FORMAT_TO_JS = {
    'pt-br': ('pt-BR', 'dd/MM/yyyy'),
    'es': ('es', 'dd/MM/yyyy'),
}

LANGUAGE_CODE = 'pt-br'

# The absolute path to the folder containing the attachments
ATTACHMENTS_FOLDER_PATH = '/home/colab/trac/attachments/'

# ORDERING_DATA receives the options to order for as it's keys and a dict as
# value, if you want to order for the last name, you can use something like:
# 'last_name': {'name': 'Last Name', 'fields': 'last_name'} inside the dict,
# you pass two major keys (name, fields)
# The major key name is the name to appear on the template
# the major key fields it show receive the name of the fields to order for in
# the indexes

ORDERING_DATA = {
    'latest':  {
        'name': gettext(u'Recent activity'),
        'fields': ('-modified', '-created'),
    },
    'hottest': {
        'name': gettext(u'Relevance'),
        'fields': None,
    },
}

# File type groupings is a tuple of tuples containg what it should filter,
# how it should be displayed, and a tuple of which mimetypes it includes
FILE_TYPE_GROUPINGS = (
    ('document', gettext(u'Document'),
     ('doc', 'docx', 'odt', 'otx', 'dotx', 'pdf', 'ott')),
    ('presentation', gettext(u'Presentation'), ('ppt', 'pptx', 'odp')),
    ('text', gettext(u'Text'), ('txt', 'po', 'conf', 'log')),
    ('code', gettext(u'Code'),
     ('py', 'php', 'js', 'sql', 'sh', 'patch', 'diff', 'html', '')),
    ('compressed', gettext(u'Compressed'), ('rar', 'zip', 'gz', 'tgz', 'bz2')),
    ('image', gettext(u'Image'),
     ('jpg', 'jpeg', 'png', 'tiff', 'gif', 'svg', 'psd', 'planner', 'cdr')),
    ('spreadsheet', gettext(u'Spreadsheet'),
     ('ods', 'xls', 'xlsx', 'xslt', 'csv')),
)


# the following variable define how many characters should be shown before
# a highlighted word, to make sure that the highlighted word will appear
HIGHLIGHT_NUM_CHARS_BEFORE_MATCH = 30
HAYSTACK_CUSTOM_HIGHLIGHTER = 'colab.utils.highlighting.ColabHighlighter'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': os.environ.get('COLAB_SOLR_URL'),
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'colab',
        'USER': 'colab',
        'PASSWORD': os.environ.get('COLAB_DEFAULT_DB_PWD'),
        'HOST': os.environ.get('COLAB_DEFAULT_DB_HOST'),
    },
    'trac': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'trac_colab',
        'USER': 'colab',
        'PASSWORD': os.environ.get('COLAB_TRAC_DB_PWD'),
        'HOST': os.environ.get('COLAB_TRAC_DB_HOST'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

DATABASE_ROUTERS = ['colab.routers.TracRouter',]

INSTALLED_APPS = INSTALLED_APPS + (

    # Not standard apps
    'raven.contrib.django.raven_compat',
    'south',
    'cliauth',
    'django_mobile',
    'django_browserid',
    'conversejs',
    'haystack',
    'hitcounter',
    'badger',

    # Own apps
    'super_archives',
    'api',
    'rss',
    'planet',
    'accounts',
    'proxy',
    'search',

    # Feedzilla and deps
    'feedzilla',
    'taggit',
    'common',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', 'console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse'
         }
     },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'filters': ['require_debug_false'],
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
            'handlers': ['sentry'],
            'level': 'WARNING',
        },
        'conversejs': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

COLAB_FROM_ADDRESS = '"Colab Interlegis" <noreply@interlegis.leg.br>'
SERVER_EMAIL = EMAIL_HOST_USER = COLAB_FROM_ADDRESS

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
    'django_mobile.context_processors.is_mobile',
    'super_archives.context_processors.mailarchive',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
)

# Add the django_browserid authentication backend.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.auth.ColabBrowserIDBackend',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'www', 'static')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

AUTH_USER_MODEL = 'accounts.User'

ALLOWED_HOSTS = ['colab.interlegis.leg.br']

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


### Feedzilla  (planet)
from feedzilla.settings import *
FEEDZILLA_PAGE_SIZE = 5
FEEDZILLA_SITE_TITLE = gettext(u'Planet Colab')
FEEDZILLA_SITE_DESCRIPTION = gettext(u'Colab blog aggregator')


### Mailman API settings
MAILMAN_API_URL = 'http://listas.interlegis.gov.br:8000'


### BrowserID / Persona
SITE_URL = 'https://colab.interlegis.leg.br'
BROWSERID_AUDIENCES = [SITE_URL]


LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = '/'
LOGOUT_REDIRECT_URL = '/'
BROWSERID_CREATE_USER = False


## Proxy settings
COLAB_TRAC_URL = 'http://colab-backend.interlegis.leg.br/'
COLAB_CI_URL = 'http://jenkins.interlegis.leg.br:8080/ci/'

REVPROXY_ADD_REMOTE_USER = True


## Converse.js settings
# This URL must use SSL in order to keep chat sessions secure
CONVERSEJS_BOSH_SERVICE_URL = SITE_URL + '/http-bind'

CONVERSEJS_AUTO_REGISTER = 'mensageiro.interlegis.gov.br'


try:
    from local_settings import *
except ImportError:
    pass
