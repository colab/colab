
from django.utils.translation import ugettext_lazy as _
from colab.plugins.utils.menu import colab_url_factory

name = '{{ app_name }}'
verbose_name = '{{ app_name_verbose }} Plugin'

upstream = 'localhost'
# middlewares = []

urls = {
    'include': '{{ app_name }}.urls',
    'prefix': '^{{ app_name }}/',
}

menu_title = _('{{ app_name }}')

url = colab_url_factory('{{ app_name }}')

# Extra data to be exposed to plugin app config
extra = {}

menu_urls = (
# Example of menu URL:
#    url(display=_('Public Projects'), viewname='{{ app_name }}',
#        kwargs={'path': 'public/projects'}, auth=False),

# Example of authenticated user menu URL:
#    url(display=_('Profile'), viewname='{{ app_name }}',
#        kwargs={'path': 'profile'}, auth=True),
)
