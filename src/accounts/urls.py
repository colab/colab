
from django.conf.urls import patterns, include, url

from .views import UserProfileDetailView


urlpatterns = patterns('',
    url(r'^$', 'accounts.views.signup', name='signup'),

    url(r'^verify/(?P<hash>[\w]{32})/$',
        'accounts.views.verify_email', name='email_verification'),

    url(r'^(?P<username>[\w@+.-]+)/?$',
        UserProfileDetailView.as_view(), name='user_profile'),

    #url(r'^user/(?P<username>[\w@+.-]+)/edit/?$',
    #    'colab.deprecated.views.userprofile.update', name='user_profile_update'),
)
