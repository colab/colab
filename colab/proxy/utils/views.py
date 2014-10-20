
from django.conf import settings

from revproxy.views import ProxyView


class ColabProxyView(ProxyView):
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_theme_template = 'base.html'
    html5 = True

    @property
    def upstream(self):
        proxy_config = settings.PROXIED_APPS.get(self.app_label, {})
        return proxy_config.get('upstream')

    @property
    def app_label(self):
        raise NotImplementedError('app_label attribute must be set')
