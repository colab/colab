# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from tastypie.api import Api

from .resources import (UserResource, EmailAddressResource, MessageResource)
from .views import VoteView


api = Api(api_name='v1')
api.register(UserResource())
api.register(EmailAddressResource())
api.register(MessageResource())


urlpatterns = patterns('',
    url(r'message/(?P<msg_id>\d+)/vote$', VoteView.as_view()),

    # tastypie urls
    url(r'', include(api.urls)),
)
