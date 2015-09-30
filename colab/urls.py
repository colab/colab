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
    url(r'^rss/', include('colab.rss.urls')),

    url(r'^account/', include('colab.accounts.urls')),
    url(r'^myaccount/(?P<route>.*)$',
        'colab.accounts.views.myaccount_redirect', name='myaccount'),

    url(r'^colab/admin/', include(admin.site.urls)),

    url(r'^archives/', include('colab.super_archives.urls')),

    url(r'', include('colab.plugins.urls')),
)
