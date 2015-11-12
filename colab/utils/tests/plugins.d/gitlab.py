from colab.plugins.utils.menu import colab_url_factory

name = "gitlab"
verbose_name = "Gitlab"

upstream = 'https://localhost/gitlab/'
private_token = 'AVA8vrohDpoSws41zd1w'

urls = {
    "include": "gitlab.urls",
    "prefix": 'gitlab/',
    "namespace": "gitlab"
}

url = colab_url_factory('gitlab')
