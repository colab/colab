from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'colab.views.other.home', name='home'),

    url(r'^archives/', include('colab.super_archives.urls')),

    url(r'^api/', include('colab.api.urls')),
    
    url(r'^rss/', include('colab.rss.urls')),

    url(r'^user/(?P<username>[\w@+.-]+)/?$',
        'colab.views.userprofile.by_username', name='user_profile'),
    
    url(r'^user/$', 'colab.views.userprofile.by_request_user', 
        name='user_profile_by_request_user'),
    
    url(r'^user/hash/(?P<emailhash>[\w]+)$',
        'colab.views.userprofile.by_emailhash'),
    
    url(r'^user/(?P<username>[\w]+)/edit/?$', 
        'colab.views.userprofile.update', name='user_profile_update'),
        
    url(r'^search/$', 'colab.views.other.search', name='search'),

    url(r'^account/$', 'colab.views.signup.signup', name='signup'), 

    url(r'^account/changepassword/$', 'colab.views.signup.change_password',
        name='change_password'),

    url(r'^account/resetpassword/$', 
        'colab.views.signup.request_reset_password', 
        name='request_reset_password'),
        
    url(r'^account/reset_password/(?P<hash>[\w]{32})/$',
        'colab.views.signup.reset_password', name='reset_password'),

    url(r'^signup/verify/(?P<hash>[\w]{32})/$', 
        'colab.views.signup.verify_email', name='email_verification'), 

    url(r'^account/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'}, name='login'),

    url(r'^account/logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}, name='logout'),
    
    # Uncomment the next line to enable the admin:
    url(r'^colab/admin/', include(admin.site.urls)),
)

