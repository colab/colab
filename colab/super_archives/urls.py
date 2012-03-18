from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
#    url(r'thread/(?P<thread>\d+)/$', 'super_archives.views.thread', name='thread'),
    url(r'thread/(?P<mailinglist>[-\w]+)/(?P<thread_token>[-\w]+)$', 
        'colab.super_archives.views.thread', name="thread_view"),
    url(r'thread/$', 
        'colab.super_archives.views.list_messages', name='thread_list')
)
