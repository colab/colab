
from django.conf import settings

from ..utils.views import ColabProxyView


class RedmineProxyView(ColabProxyView):
    upstream = settings.PROXIED_APPS['redmine']['upstream']
    diazo_theme_template = 'proxy/redmine.html'
