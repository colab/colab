from django.utils.translation import ugettext_lazy as _
from colab.plugins.utils.menu import colab_url_factory

name = "colab_gitlab"
verbose_name = "Gitlab"

upstream = 'https://localhost/gitlab/'
private_token = 'AVA8vrohDpoSws41zd1w'

urls = {
         "include":"colab_gitlab.urls",
         "prefix": 'gitlab/',
         "namespace":"gitlab"
       }

url = colab_url_factory('gitlab')

