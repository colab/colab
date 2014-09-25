
from django.conf.urls import patterns, url

from .views import (UserProfileDetailView, UserProfileUpdateView, LoginView,
                    ManageUserSubscriptionsView, ChangeXMPPPasswordView)


urlpatterns = patterns('',
    url(r'^register/$', 'colab.accounts.views.signup', name='signup'),

    url(r'^change-password/$',
        ChangeXMPPPasswordView.as_view(), name='change_password'),

    url(r'^login/?$', LoginView.as_view(), name='login'),
#    url(r'^login/?$', 'django.contrib.auth.views.login', name='login'),

#    url(r'^logout/?$',  'accounts.views.logoutColab', name='logout'),

    url(r'^(?P<username>[\w@+.-]+)/?$',
        UserProfileDetailView.as_view(), name='user_profile'),

    url(r'^(?P<username>[\w@+.-]+)/edit/?$',
        UserProfileUpdateView.as_view(), name='user_profile_update'),

    url(r'^(?P<username>[\w@+.-]+)/subscriptions/?$',
        ManageUserSubscriptionsView.as_view(), name='user_list_subscriptions'),
)
