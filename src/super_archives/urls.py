from django.conf.urls import patterns, include, url

from .views import EmailView, EmailValidationView, ThreadView, \
                   ThreadDashboardView


urlpatterns = patterns('super_archives.views',
    url(r'thread/(?P<mailinglist>[-\w]+)/(?P<thread_token>[-\w]+)$',
        ThreadView.as_view(), name="thread_view"),
    url(r'thread/$', ThreadDashboardView.as_view(), name='thread_list'),
    url(r'manage/email/validate/?$', EmailValidationView.as_view(),
                                     name="archive_email_validation_view"),
    url(r'manage/email/(?P<key>[0-9a-z]{32})?', EmailView.as_view(),
                                                name="archive_email_view"),
)
