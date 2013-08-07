
from custom_settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

SOLR_COLAB_URI = None
SOLR_HOSTNAME = None

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')(jksdfhsjkadfhjkh234ns!8fqu-1186h$vuj'

#import socks
#SOCKS_TYPE = socks.PROXY_TYPE_SOCKS5
#SOCKS_SERVER = '127.0.0.1'
#SOCKS_PORT = 9050

SITE_URL = 'http://localhost:8000'

# Path to redirect to on successful login.
LOGIN_REDIRECT_URL = '/'

# Path to redirect to on unsuccessful login attempt.
LOGIN_REDIRECT_URL_FAILURE = '/'

# Path to redirect to on logout.
LOGOUT_REDIRECT_URL = '/'
