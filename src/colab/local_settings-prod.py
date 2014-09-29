
import os
import json

from custom_settings import *

SECRETS_FILE = '/home/colab/colab/secrets.json'

if os.path.exists(SECRETS_FILE):
    secrets = json.load(file(SECRETS_FILE))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Name Surname', 'email@provider.com'),
)
MANAGERS = ADMINS

COLAB_FROM_ADDRESS = '"Colab" <noreply@domain.com>'
SERVER_EMAIL = COLAB_FROM_ADDRESS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = secrets.get('SECRET_KEY')

SITE_URL = ''
ALLOWED_HOSTS = []

# XMPP Server
CONVERSEJS_AUTO_REGISTER = ''

DATABASES['default']['PASSWORD'] = secrets.get('COLAB_DB_PWD')
DATABASES['default']['HOST'] = 'localhost'

DATABASES['trac'] = 'trac_colab'
DATABASES['trac']['PASSWORD'] = secrets.get('TRAC_DB_PWD')
DATABASES['trac']['HOST'] = 'localhost'

HAYSTACK_CONNECTIONS['default']['URL'] = 'http://localhost:8983/solr/'

COLAB_TRAC_URL = 'http://localhost:5000/trac/'
COLAB_GITLAB_URL = 'http://localhost:8090/gitlab/'

CONVERSEJS_ENABLED = False

ROBOTS_NOINDEX = False

RAVEN_CONFIG = {
    'dsn': secrets.get('RAVEN_DSN', '') + '?timeout=30',
}
