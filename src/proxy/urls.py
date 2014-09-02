
from django.conf.urls import patterns, include, url

from .views import JenkinsProxyView, GitlabProxyView, RedmineProxyView


urlpatterns = patterns('',
    # Jenkins URLs
    url(r'^ci/(?P<path>.*)$', JenkinsProxyView.as_view()),

    # Gitlab
    url(r'^gitlab/(?P<path>.*)$', GitlabProxyView.as_view()),

    # Redmine
    url(r'^redmine/(?P<path>.*)$', RedmineProxyView.as_view())
)
