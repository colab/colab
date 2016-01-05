
from colab.plugins.views import ColabProxyView


class {{ app_name_camel }}ProxyView(ColabProxyView):
    app_label = '{{ app_name }}'
