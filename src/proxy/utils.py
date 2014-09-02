
from django.conf import settings

from revproxy.views import ProxyView


class ColabProxyView(ProxyView):
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_theme_template = 'base.html'
    html5 = True
