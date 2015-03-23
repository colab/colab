
from django.conf.urls import patterns, url

from .views import NoosferoProxyView


urlpatterns = patterns('',
    # Noosfero URLs
    url(r'^(?P<path>.*)$', NoosferoProxyView.as_view(), name='noosfero'),
)
