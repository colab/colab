from django.conf.urls import patterns, include, url

from piston.resource import Resource

from .handlers import CountHandler, SearchHandler
from .views import VoteView


count_handler = Resource(CountHandler)
search_handler = Resource(SearchHandler)

urlpatterns = patterns('',
    url(r'message/(?P<msg_id>\d+)/vote$', VoteView.as_view()),
    url(r'hit/$', count_handler),
    url(r'search/$', search_handler),
)
