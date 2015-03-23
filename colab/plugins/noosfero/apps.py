
from django.utils.translation import ugettext_lazy as _

from ..utils.apps import ColabProxiedAppConfig


class ProxyNoosferoAppConfig(ColabProxiedAppConfig):
    name = 'colab.plugins.noosfero'
    verbose_name = 'Noosfero Proxy'

    menu = {
        'title': _('Social'),
        'links': (
            (_('Users'), 'search/people'),
            (_('Communities'), 'search/communities'),
        ),
        'auth_links': (
            (_('Profile'), 'profile/~/'),
            (_('Control panel'), 'myprofile/~/'),
        ),
    }
