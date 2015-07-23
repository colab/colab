
from django.conf.urls import patterns, url

from .views import GitlabProxyView, GitlabProfileProxyView

urlpatterns = patterns('',
    # Gitlab URLs
    #url(r'(?P<path>profile.*)$', GitlabProfileProxyView.as_view(), name='gitlab'),
    url(r'^(?P<path>.*)$', GitlabProxyView.as_view(), name='gitlab'),
)
