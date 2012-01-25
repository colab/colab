from django.conf.urls.defaults import patterns, include, url

from piston.resource import Resource

from colab.api.handlers import VoteHandler, CountHandler


vote_handler = Resource(VoteHandler)
count_handler = Resource(CountHandler)

urlpatterns = patterns('',
    url(r'message/(?P<message_id>\d+)/vote$', vote_handler),
    url(r'hit/$', count_handler),
)