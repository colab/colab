
from django.utils.crypto import get_random_string


CONFIG_TEMPLATE = """

## Set to false in production
DEBUG: true
TEMPLATE_DEBUG: true

## System admins
ADMINS: &admin
  -
    - John Foo
    - john@example.com
  -
    - Mary Bar
    - mary@example.com

MANAGERS: *admin

COLAB_FROM_ADDRESS: '"Colab" <noreply@example.com>'
SERVER_EMAIL: '"Colab" <noreply@example.com>'

EMAIL_HOST: localhost
EMAIL_PORT: 25
EMAIL_SUBJECT_PREFIX: '[colab]'

SECRET_KEY: '{secret_key}'

#  Must use it without trailing slash
SITE_URL: 'http://localhost:8000'
BROWSERID_AUDIENCES:
  - http://localhost:8000
#  - http://example.com
#  - https://example.org
#  - http://example.net

ALLOWED_HOSTS:
  - localhost
#  - example.com
#  - example.org
#  - example.net

### Uncomment to enable Broswer ID protocol for authentication
# BROWSERID_ENABLED: True

### Uncomment to enable Converse.js
# CONVERSEJS_ENABLED: True

### Uncomment to enable auto-registration
# CONVERSEJS_AUTO_REGISTER: 'xmpp.example.com'

## Database settings
DATABASES:
  default:
    ENGINE: django.db.backends.postgresql_psycopg2
    HOST: localhost
    NAME: colab
    USER: colab
    PASSWORD: colab

## Disable indexing
ROBOTS_NOINDEX: false

### Log errors to Sentry instance
# RAVEN_DSN: 'http://public:secret@example.com/1'

### Colab proxied apps
# PROXIED_APPS:
#   gitlab:
#     upstream: 'http://localhost:8090/gitlab/'
#     private_token: ''
#   trac:
#     upstream: 'http://localhost:5000/trac/'

"""


def initconfig():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(50, chars)
    print(CONFIG_TEMPLATE.format(secret_key=secret_key))
