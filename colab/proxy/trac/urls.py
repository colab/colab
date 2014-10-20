
from django.conf.urls import patterns, url

from .views import TracProxyView


urlpatterns = patterns('',
    # Trac
    url(r'^(?P<path>.*)$', TracProxyView.as_view()),
)
