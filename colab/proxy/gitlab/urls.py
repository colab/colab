
from django.conf.urls import patterns, url

from .views import GitlabProxyView

urlpatterns = patterns('',
    # Gitlab URLs
    url(r'^(?P<path>.*)$', GitlabProxyView.as_view(), name='gitlab'),
)
