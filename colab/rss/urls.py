from django.conf.urls.defaults import patterns, url
import feeds 

urlpatterns = patterns('',
    url(r'threads/latest/$', feeds.LatestThreadsFeeds()),
    url(r'colab/latest/$', feeds.LatestColabFeeds()),
    url(r'threads/hottest/$', feeds.HottestThreadsFeeds()),
)

