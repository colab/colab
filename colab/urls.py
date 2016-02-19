from django.conf.urls import patterns, include, url, static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
from django.views.generic import RedirectView
from accounts.views import UserProfileUpdateView
from django.views.defaults import permission_denied

admin.autodiscover()

urlpatterns = []

colab_plugins = settings.COLAB_APPS

for plugin in colab_plugins:
    colab_plugin = colab_plugins.get(plugin)
    plugin_blacklist = colab_plugin.get('blacklist')
    if plugin_blacklist:
        for plugin_url in plugin_blacklist:
            final_url = colab_plugin.get('urls').get('prefix')
            final_url += plugin_url
            urlpatterns += patterns(
                '', url(final_url, permission_denied))

if hasattr(settings, 'BLACKLIST'):
    core_blacklist = settings.BLACKLIST
    for core_url in core_blacklist:
        urlpatterns += patterns('', url(core_url, permission_denied))


urlpatterns += patterns(
    '',
    url(r'^$', RedirectView.as_view(url=settings.COLAB_HOME_URL), name='home'),
    url(r'^robots.txt$', 'colab.home.views.robots', name='robots'),
    url(r'^dashboard$', 'colab.home.views.dashboard', name='dashboard'),
    url(r'^search/', include('colab.search.urls')),
    url(r'^rss/', include('colab.rss.urls')),

    url(r'^account/', include('colab.accounts.urls')),
    url(r'^myaccount/(?P<route>.*)$',
        'colab.accounts.views.myaccount_redirect', name='myaccount'),

    url(r'^colab/admin/', include(admin.site.urls)),

    url(r'^archives/', include('colab.super_archives.urls')),

    url(r'', include('colab.plugins.urls')),
)
