
import os

from django.conf import settings

from revproxy.views import ProxyView


CWD = os.path.abspath(os.path.dirname(__file__))
DIAZO_RULES_DIR = os.path.join(CWD, 'diazo')


class JenkinsProxyView(ProxyView):
    base_url = settings.COLAB_CI_URL
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_theme_template = 'base.html'
    diazo_rules = os.path.join(DIAZO_RULES_DIR, 'jenkins.xml')
    html5 = True

class GitlabProxyView(ProxyView):
    base_url = settings.COLAB_GITLAB_URL
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_theme_template = 'proxy/gitlab.html'
    diazo_rules = os.path.join(DIAZO_RULES_DIR, 'gitlab.xml')
    html5 = True

class RedmineProxyView(ProxyView):
    base_url = settings.COLAB_REDMINE_URL
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_theme_template = 'proxy/redmine.html'
    diazo_rules = os.path.join(DIAZO_RULES_DIR, 'redmine.xml')
    html5 = True

