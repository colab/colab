
import os
import json

from custom_settings import *

SECRETS_FILE = '/home/colab/colab/secrets.json'

if os.path.exists(SECRETS_FILE):
    secrets = json.load(file(SECRETS_FILE))


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Paulo Meirelles', 'paulo@softwarelivre.org'),
)

MANAGERS = ADMINS

COLAB_FROM_ADDRESS = '"Portal do Software Publico" <noreply@beta.softwarepublico.gov.br>'
SERVER_EMAIL = COLAB_FROM_ADDRESS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = secrets.get('SECRET_KEY')

SITE_URL = 'http://beta.softwarepublico.gov.br'
BROWSERID_AUDIENCES = [SITE_URL, SITE_URL.replace('https', 'http')]

ALLOWED_HOSTS = ['beta.softwarepublico.gov.br']

INTERNAL_IPS = ('127.0.0.1', )

DATABASES['default']['PASSWORD'] = secrets.get('COLAB_DB_PWD')
DATABASES['default']['HOST'] = 'localhost'

TRAC_ENABLED = True

if TRAC_ENABLED:
    from trac_settings import *
    DATABASES['trac'] = TRAC_DATABASE
    DATABASES['trac']['PASSWORD'] = secrets.get('TRAC_DB_PWD')
    DATABASES['trac']['HOST'] = 'localhost'

HAYSTACK_CONNECTIONS['default']['URL'] = 'http://localhost:8983/solr/'

COLAB_TRAC_URL = 'http://localhost:5000/trac/'
COLAB_CI_URL = 'http://localhost:8080/ci/'
COLAB_GITLAB_URL = 'http://localhost:8090/gitlab/'
COLAB_REDMINE_URL = 'http://localhost:9080/redmine/'

CONVERSEJS_ENABLED = False

DIAZO_THEME = SITE_URL

ROBOTS_NOINDEX = True

RAVEN_CONFIG = {
    'dsn': secrets.get('RAVEN_DSN', '') + '?timeout=30',
}
