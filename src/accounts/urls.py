
from django.conf.urls import patterns, include, url

from .views import UserProfileDetailView, UserProfileUpdateView, \
                   ManageUserSubscriptionsView


urlpatterns = patterns('',
    url(r'^register/$', 'accounts.views.signup', name='signup'),

    url(r'^(?P<username>[\w@+.-]+)/?$',
        UserProfileDetailView.as_view(), name='user_profile'),

    url(r'^(?P<username>[\w@+.-]+)/edit/?$',
        UserProfileUpdateView.as_view(), name='user_profile_update'),

    url(r'^(?P<username>[\w@+.-]+)/subscriptions/?$',
        ManageUserSubscriptionsView.as_view(), name='user_list_subscriptions'),
)
