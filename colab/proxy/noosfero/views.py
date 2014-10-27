
from django.conf import settings

from ..utils.views import ColabProxyView


class NoosferoProxyView(ColabProxyView):
    app_label = 'noosfero'
    diazo_theme_template = 'proxy/noosfero.html'
