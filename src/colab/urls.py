
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'colab.deprecated.views.other.home', name='home'),

    url(r'^search/$', 'colab.deprecated.views.other.search', name='search'),

    url(r'open-data/$', TemplateView.as_view(template_name='open-data.html'),
        name='opendata'),

    url(r'^archives/', include('super_archives.urls')),

    url(r'^api/', include('api.urls')),

    url(r'^rss/', include('rss.urls')),

    url(r'^user/', include('accounts.urls')),    # Kept for backwards compatibility
    url(r'^signup/', include('accounts.urls')),  # (same here) TODO: move to nginx
    url(r'^account/', include('accounts.urls')),

    url(r'^planet/', include('feedzilla.urls')),

    url(r'^browserid/', include('django_browserid.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^colab/admin/', include(admin.site.urls)),

    # Trac URLs
    url(u'^(?P<path>(?:admin|wiki|changeset|newticket|ticket|chrome|timeline|roadmap|browser|report|tags|query|about|prefs|log|attachment|raw-attachment).*)$',
        'revproxy.views.proxy', {'base_url': settings.COLAB_TRAC_URL})
)
