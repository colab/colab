
from django.conf.urls import patterns, include, url

from .views import TracProxyView


urlpatterns = patterns('',
    # Trac URLs
    url(r'^(?P<path>(?:admin|wiki|changeset|newticket|ticket|chrome|timeline|roadmap|browser|report|tags|query|about|prefs|log|attachment|raw-attachment|diff|milestone).*)$',
        TracProxyView.as_view()),

      # Trac
      url(r'^trac/(?P<path>.*)$', TracProxyView.as_view()),
)
