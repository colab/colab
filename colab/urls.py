from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'colab.views.home', name='home'),

    url(r'^archives/', include('colab.super_archives.urls')),

    url(r'^api/', include('colab.api.urls')),

    url(r'^user/hash/(?P<emailhash>[\w]+)$',
        'colab.views.user_profile_emailhash'),

    url(r'^user/(?P<username>[\w]+)/?$', 'colab.views.user_profile_username'),
    
    url(r'^user/(?P<username>[\w]+)/edit/?$', 
        'colab.views.user_profile_edit'),

    url(r'^user/$',
        'colab.views.user_profile_empty'),

    url(r'^signup/$', 'colab.views.signup'), 

    url(r'^login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'}),

    url(r'^logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
