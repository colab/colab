
import os

from django.conf import settings

from revproxy.views import ProxyView


CWD = os.path.abspath(os.path.dirname(__file__))
DIAZO_RULES_DIR = os.path.join(CWD, 'diazo')


class TracProxyView(ProxyView):
    base_url = settings.COLAB_TRAC_URL
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_theme_template = 'base.html'
    diazo_rules = os.path.join(DIAZO_RULES_DIR, 'trac.xml')


class JenkinsProxyView(ProxyView):
    base_url = settings.COLAB_CI_URL
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_theme_template = 'base.html'
    diazo_rules = os.path.join(DIAZO_RULES_DIR, 'jenkins.xml')
