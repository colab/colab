
from django.conf.urls import patterns, url

from .views import GitlabProxyView, GitlabProfileProxyView

urlpatterns = patterns('',
    url(r'^(?P<path>.*)$', GitlabProxyView.as_view(), name='gitlab'),
)
