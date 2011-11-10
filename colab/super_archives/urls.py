from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
#    url(r'thread/(?P<thread>\d+)/$', 'super_archives.views.thread', name='thread'),
    url(r'thread/(?P<thread_token>[-\w]+)$', 'super_archives.views.thread'),
    url(r'thread/$', 'super_archives.views.list_messages')
)
