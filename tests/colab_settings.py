
## Set to false in production
DEBUG = False
TEMPLATE_DEBUG = False

## System admins
ADMINS = [['John Foo', 'john@example.com'], ['Mary Bar', 'mary@example.com']]

MANAGERS = ADMINS

COLAB_FROM_ADDRESS = '"Colab" <noreply@example.com>'
SERVER_EMAIL = '"Colab" <noreply@example.com>'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = '[colab]'

SECRET_KEY = 'not-a-secret'

ALLOWED_HOSTS = [
    'localhost',
#    'example.com',
#    'example.org',
#    'example.net',
]

### Uncomment to enable social networks fields profile
# SOCIAL_NETWORK_ENABLED = True

## Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'colab.sqlite3',
    }
}

## Disable indexing
ROBOTS_NOINDEX = True

LOGGING = {
    'version': 1,

    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },

    'loggers': {
        'colab.mailman': {
            'handlers': ['null'],
            'propagate': False,
        },
        'haystack': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}
