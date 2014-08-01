import os


TRAC_DATABASE = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'trac_colab',
    'USER': 'colab',
    'PASSWORD': os.environ.get('COLAB_TRAC_DB_PWD'),
    'HOST': os.environ.get('COLAB_TRAC_DB_HOST'),
}

COLAB_TRAC_URL = 'localhost:5000/trac/'
