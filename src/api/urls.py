from django.conf.urls.defaults import patterns, include, url

from piston.resource import Resource

from colab.api.handlers import VoteHandler, CountHandler, SearchHandler


vote_handler = Resource(VoteHandler)
count_handler = Resource(CountHandler)
search_handler = Resource(SearchHandler)

urlpatterns = patterns('',
    url(r'message/(?P<message_id>\d+)/vote$', vote_handler),
    url(r'hit/$', count_handler),
    url(r'search/$', search_handler),
)
