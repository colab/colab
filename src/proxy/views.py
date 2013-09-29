
import os

from django.conf import settings

from revproxy.views import ProxyView


class TracProxyView(ProxyView):
    base_url = settings.COLAB_TRAC_URL
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_template_theme = 'base.html'
    diazo_rules = os.path.join(settings.BASE_DIR, 'proxy', 'trac_rules.xml')


class JenkinsProxyView(ProxyView):
    base_url = settings.COLAB_CI_URL
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_template_theme = 'base.html'
