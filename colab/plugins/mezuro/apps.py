from django.utils.translation import ugettext_lazy as _
from ..utils.apps import ColabProxiedAppConfig

class ProxyMezuroAppConfig(ColabProxiedAppConfig):
    name = 'colab.plugins.mezuro'
    verbose_name = 'Mezuro Proxy'
