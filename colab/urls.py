from django.conf.urls import patterns, include, url, static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=settings.COLAB_HOME_URL), name='home'),
    url(r'^robots.txt$', 'colab.home.views.robots', name='robots'),
    url(r'^dashboard$', 'colab.home.views.dashboard', name='dashboard'),
    url(r'^search/', include('colab.search.urls')),
    url(r'^api/', include('colab.api.urls')),
    url(r'^rss/', include('colab.rss.urls')),

    url(r'^account/', include('colab.accounts.urls')),
    url(r'^myaccount/(?P<route>.*)$',
        'colab.accounts.views.myaccount_redirect', name='myaccount'),

    url(r'^colab/admin/', include(admin.site.urls)),

    url(r'^archives/', include('colab.super_archives.urls')),
    url(r'^gitlab/', include('colab.plugins.gitlab.urls')),
    url(r'^mezuro/', include('colab.plugins.mezuro.urls')),
    url(r'^social/', include('colab.plugins.noosfero.urls')),

    url(r'', include('colab.plugins.urls')),
)

if settings.DEBUG:
    urlpatterns += static.static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
