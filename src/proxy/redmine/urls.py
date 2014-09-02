
from django.conf.urls import patterns, url

from .views import RedmineProxyView


urlpatterns = patterns('',
    # RedmineProxyView URLs
    url(r'^redmine/(?P<path>.*)$', RedmineProxyView.as_view()),
)
