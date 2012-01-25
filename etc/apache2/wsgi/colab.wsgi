import site
import os

cwd_path = os.path.abspath(os.path.dirname(__file__))
virtualenv_path = os.path.join(cwd_path, '../lib/python2.6/site-packages')
site.addsitedir(virtualenv_path)

from django.core.handlers.wsgi import WSGIHandler
os.environ['DJANGO_SETTINGS_MODULE'] = 'colab.settings'
application = WSGIHandler()


