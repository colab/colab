
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^$', 'accounts.views.signup', name='signup'),

    url(r'^verify/(?P<hash>[\w]{32})/$',
        'accounts.views.verify_email', name='email_verification'),

    # TODO: review and redo those weird views from 
    #   colab.deprecated.views.userprofile moving them to accounts.views 
    url(r'^user/(?P<username>[\w@+.-]+)/?$',
        'colab.deprecated.views.userprofile.by_username', name='user_profile'),

    url(r'^user/$', 'colab.deprecated.views.userprofile.by_request_user',
        name='user_profile_by_request_user'),

    url(r'^user/hash/(?P<emailhash>[\w]+)$',
        'colab.deprecated.views.userprofile.by_emailhash'),

    url(r'^user/(?P<username>[\w@+.-]+)/edit/?$',
        'colab.deprecated.views.userprofile.update', name='user_profile_update'),
)
