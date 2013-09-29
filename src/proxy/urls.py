
from django.conf.urls import patterns, include, url

from .views import TracProxyView, JenkinsProxyView


urlpatterns = patterns('',
    # Trac URLs
    url(r'^(?P<path>(?:admin|wiki|changeset|newticket|ticket|chrome|timeline|roadmap|browser|report|tags|query|about|prefs|log|attachment|raw-attachment).*)$',
	TracProxyView.as_view()),

    # Jenkins URLs
    url(r'^ci/(?P<path>.*)$', JenkinsProxyView.as_view()),
)
