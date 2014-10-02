"""
WSGI config for colab project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "colab.settings")
os.environ.setdefault("COLAB_SETTINGS", "/etc/colab/settings.yaml")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
