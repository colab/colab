
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from colab.accounts.views import (UserProfileDetailView, UserProfileUpdateView,
                                  EmailValidationView, EmailView, SignupView)

from colab.accounts.forms import (ColabSetPasswordForm,
                                  ColabPasswordChangeForm)

urlpatterns = patterns('',
    url(r'^login/?$', 'django.contrib.auth.views.login',
        {'redirect_field_name': 'previous_path'}, name='login'),

    url(r'^logout/?$', 'django.contrib.auth.views.logout',
        {'next_page': 'home'}, name='logout'),

    url(r'^password-reset-done/?$', 'colab.accounts.views.password_reset_done_custom',
        name="password_reset_done"),

    url(r'^password-reset-complete/$', 'colab.accounts.views.password_reset_complete_custom',
        name="password_reset_complete"),

    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm_custom.html',
         'set_password_form': ColabSetPasswordForm},
        name="password_reset_confirm"),

    url(r'^password-reset/?$', auth_views.password_reset,
        {'template_name': 'registration/password_reset_form_custom.html'},
        name="password_reset"),

    url(r'^change-password/?$', auth_views.password_change,
        {'template_name': 'registration/password_change_form_custom.html',
         'password_change_form': ColabPasswordChangeForm},
        name='password_change'),

    url(r'^change-password-done/?$',
        'colab.accounts.views.password_changed', name='password_change_done'),
)

urlpatterns += patterns('',
    url(r'^register/?$', SignupView.as_view(), name='signup'),

    url(r'^(?P<username>[\w@+.-]+)/?$',
        UserProfileDetailView.as_view(), name='user_profile'),

    url(r'^(?P<username>[\w@+.-]+)/edit/?$',
        UserProfileUpdateView.as_view(), name='user_profile_update'),

    url(r'^manage/email/validate/?$', EmailValidationView.as_view(),
        name="email_validation_view"),

    url(r'^manage/email/(?P<key>[0-9a-z]{32})?', EmailView.as_view(),
        name="email_view"),
)
