"""
Django settings for colab project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)

# Used for settings translation
from django.utils.translation import ugettext_lazy as _

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ""

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DATABASE_ROUTERS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # First app to provide AUTH_USER_MODEL to others
    'colab.accounts',

    # Not standard apps
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
    'colab.home',
    'colab.super_archives',
    'colab.api',
    'colab.rss',
    'colab.planet',
    'colab.search',
    'colab.badger',
    'colab.tz',

    # Feedzilla and deps
    'feedzilla',
    'taggit',
    'common',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'colab.urls'

WSGI_APPLICATION = 'colab.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = '/usr/share/nginx/colab/static/'
MEDIA_ROOT = '/usr/share/nginx/colab/media/'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'


# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)


# Allow Django runserver to serve SVG files
#   https://code.djangoproject.com/ticket/20162
import mimetypes
mimetypes.add_type('image/svg+xml', '.svg')

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
        'URL': 'http://localhost:8983/solr/',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

DATABASE_ROUTERS = []


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django_mobile.context_processors.is_mobile',
    'colab.super_archives.context_processors.mailarchive',
    'colab.proxy.context_processors.proxied_apps',
    'colab.home.context_processors.robots',
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
    'colab.tz.middleware.TimezoneMiddleware',
)

# Add the django_browserid authentication backend.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'colab.accounts.auth.ColabBrowserIDBackend',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

AUTH_USER_MODEL = 'accounts.User'

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
MAILMAN_API_URL = 'http://localhost:9000'

### BrowserID / Persona
SITE_URL = 'http://localhost:8000'
BROWSERID_AUDIENCES = [SITE_URL, SITE_URL.replace('https', 'http')]


LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = '/'
LOGOUT_REDIRECT_URL = '/user/logout'
BROWSERID_CREATE_USER = False

REVPROXY_ADD_REMOTE_USER = True

## Converse.js settings
# This URL must use SSL in order to keep chat sessions secure
CONVERSEJS_BOSH_SERVICE_URL = SITE_URL + '/http-bind'

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
DPASTE_DEFAULT_GIST_DESCRIPTION = 'Gist created from Colab DPaste'
DPASTE_DEFAULT_GIST_NAME = 'colab_paste'
DPASTE_LEXER_DEFAULT = 'text'

from .utils.conf import load_yaml_settings
locals().update(load_yaml_settings())

if locals().get('RAVEN_DSN', False):
    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN + '?timeout=30',
    }
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

proxied_apps = locals().get('PROXIED_APPS') or {}
for app_label in proxied_apps.keys():
    INSTALLED_APPS += ('colab.proxy.{}'.format(app_label),)
