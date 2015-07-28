# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from .views import VoteView


urlpatterns = patterns('',
    url(r'message/(?P<msg_id>\d+)/vote$', VoteView.as_view()),
)
