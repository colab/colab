
from django.conf import settings

from ..utils.views import ColabProxyView


class NoosferoProxyView(ColabProxyView):
    app_label = 'noosfero'
    diazo_theme_template = 'proxy/noosfero.html'
    rewrite = (
        ('^/social/account/login(.*)$', r'{}\1'.format(settings.LOGIN_URL)),
    )
