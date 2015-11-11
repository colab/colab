from django.utils.translation import ugettext_lazy as _
from colab.plugins.utils.menu import colab_url_factory

name = "colab_noosfero"
verbose_name = "Noosfero"
private_token = "ef9a334177c620b68e75a89844e8a402"

upstream = 'http://localhost/social/'

urls = {
         "include":"colab_noosfero.urls",
         "prefix": '^social/',
         "namespace":"social"
       }

url = colab_url_factory('social')

