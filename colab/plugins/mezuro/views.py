
from colab.plugins.views import ColabProxyView


class MezuroProxyView(ColabProxyView):
    app_label = 'mezuro'
    diazo_theme_template = 'proxy/mezuro.html'
