from django.conf.urls import patterns, include, url, static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^robots.txt$', 'colab.home.views.robots', name='robots'),
    url(r'^dashboard$', 'colab.home.views.dashboard', name='dashboard'),
    url(r'^$', RedirectView.as_view(url=settings.COLAB_HOME_URL), name='home'),

    url(r'^open-data/$', TemplateView.as_view(template_name='open-data.html'),
        name='opendata'),

    url(r'^search/', include('colab.search.urls')),
    url(r'^archives/', include('colab.super_archives.urls')),
    url(r'^api/', include('colab.api.urls')),
    url(r'^rss/', include('colab.rss.urls')),

    # Kept for backwards compatibility
    url(r'^user/', include('colab.accounts.urls')),
    # Kept for backwards compatibility
    url(r'^user/', include('colab.accounts.urls')),
    # (same here) TODO: move to nginx
    url(r'^signup/', include('colab.accounts.urls')),
    url(r'^account/', include('colab.accounts.urls')),
    url(r'^myaccount/(?P<route>.*)$',
        'colab.accounts.views.myaccount_redirect', name='myaccount'),

    url(r'', include('django_browserid.urls')),

    url(r'^planet/', include('feedzilla.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^colab/admin/', include(admin.site.urls)),

    url(r'^trac/', include('colab.proxy.trac.urls')),
    url(r'^gitlab/', include('colab.proxy.gitlab.urls')),
    url(r'^social/', include('colab.proxy.noosfero.urls')),
    url(r'^ci/', include('colab.proxy.jenkins.urls')),

    url(r'', include('colab.plugins.urls')),
)

if settings.DEBUG:
    urlpatterns += static.static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
