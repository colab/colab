from django.conf.urls.defaults import patterns, include, url

from piston.resource import Resource

from api.handlers import VoteHandler


vote_handler = Resource(VoteHandler)

urlpatterns = patterns('',
    url(r'message/(?P<message_id>\d+)/vote$', vote_handler),
)