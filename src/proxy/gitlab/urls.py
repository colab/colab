
from django.conf.urls import patterns, url

from .views import GitlabProxyView


urlpatterns = patterns('',
    # Gitlab URLs
    url(r'^gitlab/(?P<path>.*)$', GitlabProxyView.as_view()),
)
