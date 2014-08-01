
from django.conf.urls import patterns, include, url

from .views import ProxyView, JenkinsProxyView, GitlabProxyView, RedmineProxyView, TracProxyView 


urlpatterns = patterns('',
    # Trac URLs
    url(r'^(?P<path>(?:admin|wiki|changeset|newticket|ticket|chrome|timeline|roadmap|browser|report|tags|query|about|prefs|log|attachment|raw-attachment|diff|milestone).*)$',
        TracProxyView.as_view()),

    # Jenkins URLs
    url(r'^ci/(?P<path>.*)$', JenkinsProxyView.as_view()),

    # Trac
    url(r'^trac/(?P<path>.*)$', TracProxyView.as_view()),

    # Gitlab
    url(r'^gitlab/(?P<path>.*)$', GitlabProxyView.as_view()),

    # Redmine
    url(r'^redmine/(?P<path>.*)$', RedmineProxyView.as_view())

)
