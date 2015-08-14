
from colab.plugins.views import ColabProxyView


class GitlabProxyView(ColabProxyView):
    app_label = 'gitlab'
    diazo_theme_template = 'proxy/gitlab.html'
