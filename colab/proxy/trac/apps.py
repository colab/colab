
from django.utils.translation import ugettext_lazy as _

from ..utils.apps import ColabProxiedAppConfig


class ProxyTracAppConfig(ColabProxiedAppConfig):
    name = 'colab.proxy.trac'
    verbose_name = 'Trac Proxy'

    menu = {
        'title': _('Code'),
        'links': (
            (_('Timeline'), 'timeline'),
            (_('Wiki'), 'wiki'),
            (_('View Tickets'), 'report'),
            (_('Roadmap'), 'roadmap'),
            (_('Browse Source'), 'browser'),
        ),
        'auth_links': (
            (_('New Ticket'), 'newticket'),
            (_('New Wiki Page'), 'wiki/WikiNewPage'),
        ),
    }

    collaboration_models = []
