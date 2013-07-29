from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'colab.deprecated.views.other.home', name='home'),

    url(r'^archives/', include('super_archives.urls')),
    
    url(r'^api/', include('api.urls')),
    
    url(r'^rss/', include('rss.urls')),

    url(r'open-data/$', TemplateView.as_view(template_name='open-data.html'), 
        name='opendata'),

    url(r'^user/(?P<username>[\w@+.-]+)/?$',
        'colab.deprecated.views.userprofile.by_username', name='user_profile'),
    
    url(r'^user/$', 'colab.deprecated.views.userprofile.by_request_user', 
        name='user_profile_by_request_user'),
    
    url(r'^user/hash/(?P<emailhash>[\w]+)$',
        'colab.deprecated.views.userprofile.by_emailhash'),
    
    url(r'^user/(?P<username>[\w@+.-]+)/edit/?$', 
        'colab.deprecated.views.userprofile.update', name='user_profile_update'),
        
    url(r'^search/$', 'colab.deprecated.views.other.search', name='search'),

    url(r'^account/$', 'colab.deprecated.views.signup.signup', name='signup'), 

    url(r'^account/changepassword/$', 'colab.deprecated.views.signup.change_password',
        name='change_password'),

    url(r'^account/resetpassword/$', 
        'colab.deprecated.views.signup.request_reset_password', 
        name='request_reset_password'),
        
    url(r'^account/reset_password/(?P<hash>[\w]{32})/$',
        'colab.deprecated.views.signup.reset_password', name='reset_password'),

    url(r'^signup/verify/(?P<hash>[\w]{32})/$', 
        'colab.deprecated.views.signup.verify_email', name='email_verification'), 

    url(r'^account/login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'login.html'}, name='login'),

    url(r'^account/logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}, name='logout'),

    url(r'^planet/', include('feedzilla.urls')),
    
    # Uncomment the next line to enable the admin:
    url(r'^colab/admin/', include(admin.site.urls)),
)

