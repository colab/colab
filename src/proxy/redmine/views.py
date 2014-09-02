
from django.conf import settings

from ..utils import ColabProxyView


class RedmineProxyView(ColabProxyView):
    upstream = settings.COLAB_REDMINE_URL
    diazo_theme_template = 'proxy/redmine.html'
