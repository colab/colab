from django.conf.urls import patterns, include, url

urlpatterns = patterns('super_archives.views',
#    url(r'thread/(?P<thread>\d+)/$', 'thread', name='thread'),
    url(r'thread/(?P<mailinglist>[-\w]+)/(?P<thread_token>[-\w]+)$', 'thread', 
        name="thread_view"),
    url(r'thread/$', 'list_messages', name='thread_list')
)
