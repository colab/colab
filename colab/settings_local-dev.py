
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'colab.db',
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')(jksdfhsjkadfhjkh234ns!8fqu-1186h$vuj'

import socks
SOCKS_TYPE = socks.PROXY_TYPE_SOCKS5
SOCKS_SERVER = '127.0.0.1'
SOCKS_PORT = 9050

