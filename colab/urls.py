from django.conf.urls import patterns, include, url, static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin

from .accounts.models import User
from .search.forms import ColabSearchForm
from .super_archives.models import Message


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'colab.home.views.index', name='home'),
    url(r'^robots.txt$', 'colab.home.views.robots', name='robots'),

    url(r'^open-data/$', TemplateView.as_view(template_name='open-data.html'),
        name='opendata'),

    url(r'^search/', include('colab.search.urls')),
    url(r'^archives/', include('colab.super_archives.urls')),
    url(r'^api/', include('colab.api.urls')),
    url(r'^rss/', include('colab.rss.urls')),

    url(r'^user/', include('colab.accounts.urls')),    # Kept for backwards compatibility
    url(r'^signup/', include('colab.accounts.urls')),  # (same here) TODO: move to nginx
    url(r'^account/', include('colab.accounts.urls')),

    url(r'', include('django_browserid.urls')),

    url(r'^planet/', include('feedzilla.urls')),

    url(r'paste/', include('dpaste.urls.dpaste')),

    # Uncomment the next line to enable the admin:
    url(r'^colab/admin/', include(admin.site.urls)),

    url(r'^trac/', include('colab.proxy.trac.urls')),
    url(r'^gitlab/', include('colab.proxy.gitlab.urls')),
)

if settings.DEBUG:
    urlpatterns += static.static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
