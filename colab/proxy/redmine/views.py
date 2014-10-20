
from django.conf import settings

from ..utils.views import ColabProxyView


class RedmineProxyView(ColabProxyView):
    app_label = 'redmine'
    diazo_theme_template = 'proxy/redmine.html'
