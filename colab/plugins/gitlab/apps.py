
from django.utils.translation import ugettext_lazy as _

from ..utils.apps import ColabProxiedAppConfig


class ProxyGitlabAppConfig(ColabProxiedAppConfig):
    name = 'colab.plugins.gitlab'
    verbose_name = 'Gitlab Proxy'

    menu = {
        'title': _('Code'),
        'links': (
            (_('Public Projects'), 'public/projects'),
        ),
        'auth_links': (
            (_('Profile'), 'profile'),
            (_('New Project'), 'projects/new'),
            (_('Projects'), 'dashboard/projects'),
            (_('Groups'), 'profile/groups'),
            (_('Issues'), 'dashboard/issues'),
            (_('Merge Requests'), 'dashboard/merge_requests'),

        ),
    }
