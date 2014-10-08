
from django.conf.urls import patterns, url

from .views import (UserProfileDetailView, UserProfileUpdateView, LoginView,
                    ManageUserSubscriptionsView, ChangeXMPPPasswordView)

from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^register/$', 'colab.accounts.views.signup', name='signup'),

    url(r'^password-reset-done/?$',
        'django.contrib.auth.views.password_reset_done',
        name="password_reset_done"),

    url(r'^password-reset-complete/$',
        'django.contrib.auth.views.password_reset_complete',
        name="password_reset_complete"),

    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        name="password_reset_confirm"),

    url(r'^password-reset/?$',
        'django.contrib.auth.views.password_reset', name="password_reset"),

    url(r'^change-password/?$',
        auth_views.password_change,
        {'template_name': 'registration/password_change.html'},
        name='password_change'),

    url(r'^change-password-done/?$',
        'accounts.views.password_changed', name='password_change_done'),

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
