
from django.conf.urls import patterns, url

from .views import JenkinsProxyView


urlpatterns = patterns('',
    # Jenkins URLs
    url(r'^ci/(?P<path>.*)$', JenkinsProxyView.as_view()),
)
