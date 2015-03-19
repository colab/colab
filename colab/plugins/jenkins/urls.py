
from django.conf.urls import patterns, url

from .views import JenkinsProxyView


urlpatterns = patterns('',
    # Jenkins URLs
    url(r'^(?P<path>.*)$', JenkinsProxyView.as_view(), name='jenkins'),
)
