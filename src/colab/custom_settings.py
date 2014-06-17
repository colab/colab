from settings import *
from django.utils.translation import ugettext_lazy as _

DEBUG = False

TEMPLATE_DEBUG = False

LANGUAGES = (
    ('en', _('English')),
    ('pt-br', _('Portuguese')),
    ('es', _('Spanish')),
)

DJANGO_DATE_FORMAT_TO_JS = {
    'pt-br': ('pt-BR', 'dd/MM/yyyy'),
    'es': ('es', 'dd/MM/yyyy'),
}

LANGUAGE_CODE = 'en'

# The absolute path to the folder containing the attachments
ATTACHMENTS_FOLDER_PATH = '/mnt/trac/attachments/'

# ORDERING_DATA receives the options to order for as it's keys and a dict as
# value, if you want to order for the last name, you can use something like:
# 'last_name': {'name': 'Last Name', 'fields': 'last_name'} inside the dict,
# you pass two major keys (name, fields)
# The major key name is the name to appear on the template
# the major key fields it show receive the name of the fields to order for in
# the indexes

ORDERING_DATA = {
    'latest':  {
        'name': _(u'Recent activity'),
        'fields': ('-modified', '-created'),
    },
    'hottest': {
        'name': _(u'Relevance'),
        'fields': None,
    },
}

# File type groupings is a tuple of tuples containg what it should filter,
# how it should be displayed, and a tuple of which mimetypes it includes
FILE_TYPE_GROUPINGS = (
    ('document', _(u'Document'),
     ('doc', 'docx', 'odt', 'otx', 'dotx', 'pdf', 'ott')),
    ('presentation', _(u'Presentation'), ('ppt', 'pptx', 'odp')),
    ('text', _(u'Text'), ('txt', 'po', 'conf', 'log')),
    ('code', _(u'Code'),
     ('py', 'php', 'js', 'sql', 'sh', 'patch', 'diff', 'html', '')),
    ('compressed', _(u'Compressed'), ('rar', 'zip', 'gz', 'tgz', 'bz2')),
    ('image', _(u'Image'),
     ('jpg', 'jpeg', 'png', 'tiff', 'gif', 'svg', 'psd', 'planner', 'cdr')),
    ('spreadsheet', _(u'Spreadsheet'),
     ('ods', 'xls', 'xlsx', 'xslt', 'csv')),
)


# the following variable define how many characters should be shown before
# a highlighted word, to make sure that the highlighted word will appear
HIGHLIGHT_NUM_CHARS_BEFORE_MATCH = 30
HAYSTACK_CUSTOM_HIGHLIGHTER = 'colab.utils.highlighting.ColabHighlighter'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': os.environ.get('COLAB_SOLR_URL', 'http://localhost:8983/solr'),
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
    'i18n_model',
    'mptt',
    'dpaste',

    # Own apps
    'super_archives',
    'api',
    'rss',
    'planet',
    'accounts',
    'proxy',
    'search',
    'badger',
    'tz',

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
            'propagate': False,
        },
        'conversejs': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

COLAB_FROM_ADDRESS = '"Colab Interlegis" <noreply@interlegis.leg.br>'
SERVER_EMAIL = COLAB_FROM_ADDRESS
EMAIL_HOST = 'smtp.interlegis.leg.br'
EMAIL_PORT = 25

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
    'home.context_processors.robots',
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
    'tz.middleware.TimezoneMiddleware',
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
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'www', 'media')

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
FEEDZILLA_SITE_TITLE = _(u'Planet Colab')
FEEDZILLA_SITE_DESCRIPTION = _(u'Colab blog aggregator')


### Mailman API settings
MAILMAN_API_URL = 'localhost:8000'


### BrowserID / Persona
SITE_URL = 'localhost:8000'
BROWSERID_AUDIENCES = [SITE_URL, SITE_URL.replace('https', 'http')]


LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = '/'
LOGOUT_REDIRECT_URL = '/user/logout'
BROWSERID_CREATE_USER = False


## Proxy settings
COLAB_TRAC_URL = 'localhost:5000/trac/'
COLAB_CI_URL = 'localhost:9000/ci/'

REVPROXY_ADD_REMOTE_USER = True


## Converse.js settings
# This URL must use SSL in order to keep chat sessions secure
CONVERSEJS_BOSH_SERVICE_URL = SITE_URL + '/http-bind'

CONVERSEJS_AUTO_REGISTER = 'mensageiro.interlegis.gov.br'
CONVERSEJS_ALLOW_CONTACT_REQUESTS = False
CONVERSEJS_SHOW_ONLY_ONLINE_USERS = True


# Tastypie settings
TASTYPIE_DEFAULT_FORMATS = ['json', ]


# Dpaste settings
DPASTE_EXPIRE_CHOICES = (
    ('onetime', _(u'One Time Snippet')),
    (3600, _(u'In one hour')),
    (3600 * 24 * 7, _(u'In one week')),
    (3600 * 24 * 30, _(u'In one month')),
    ('never', _(u'Never')),
)
DPASTE_EXPIRE_DEFAULT = DPASTE_EXPIRE_CHOICES[4][0]
DPASTE_DEFAULT_GIST_DESCRIPTION = 'Gist created on Colab Interlegis'
DPASTE_DEFAULT_GIST_NAME = 'colab_paste'

try:
    from local_settings import *
except ImportError:
    pass
