from django.conf.urls import patterns, include, url

from piston.resource import Resource

from .handlers import SearchHandler
from .views import VoteView

search_handler = Resource(SearchHandler)

urlpatterns = patterns('',
    url(r'message/(?P<msg_id>\d+)/vote$', VoteView.as_view()),
    url(r'search/$', search_handler),
)
