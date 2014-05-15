from django.conf.urls import patterns, include, url, static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin

from accounts.models import User
from search.forms import ColabSearchForm
from super_archives.models import Message


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.index', name='home'),
    url(r'^robots.txt$', 'home.views.robots', name='robots'),

    url(r'^open-data/$', TemplateView.as_view(template_name='open-data.html'),
        name='opendata'),

    url(r'^search/', include('search.urls')),
    url(r'^archives/', include('super_archives.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^rss/', include('rss.urls')),

    url(r'^user/', include('accounts.urls')),    # Kept for backwards compatibility
    url(r'^signup/', include('accounts.urls')),  # (same here) TODO: move to nginx
    url(r'^account/', include('accounts.urls')),

    url(r'', include('django_browserid.urls')),

    url(r'^planet/', include('feedzilla.urls')),

    url(r'paste/', include('dpaste.urls.dpaste')),

    # Uncomment the next line to enable the admin:
    url(r'^colab/admin/', include(admin.site.urls)),

    url(r'^', include('proxy.urls')),
)

if settings.DEBUG:
    urlpatterns += static.static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
