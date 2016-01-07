from django.conf.urls import patterns, url

from .views import (EmailView, EmailValidationView, ThreadView,
                    ThreadDashboardView, VoteView, MailingListView)


urlpatterns = patterns(
    'super_archives.views',
    url(r'thread/(?P<mailinglist>[-.\w]+)/(?P<thread_token>[-.\w]+)$',
        ThreadView.as_view(), name="thread_view"),
    url(r'thread/$', ThreadDashboardView.as_view(), name='thread_list'),
    url(r'manage/email/validate/?$', EmailValidationView.as_view(),
        name="archive_email_validation_view"),
    url(r'manage/email/(?P<key>[0-9a-z]{32})?', EmailView.as_view(),
        name="archive_email_view"),
    url(r'message/(?P<msg_id>\d+)/vote$', VoteView.as_view()),
    url(r'mailinglist/(?P<mailinglist>[-.\w]+)$',
        MailingListView.as_view(), name="mailinglist_view"),
)
