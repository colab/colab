
from django.conf import settings

from ..utils.views import ColabProxyView


class GitlabProxyView(ColabProxyView):
    upstream = settings.PROXIED_APPS['gitlab']['upstream']
    diazo_theme_template = 'proxy/gitlab.html'
