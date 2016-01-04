
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import ColabSetUsernameForm, UserChangeForm

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = ColabSetUsernameForm

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name',
                                         'last_name',
                                         'twitter',
                                         'facebook',
                                         'google_talk',
                                         'webpage')}),
        (_('Permissions'), {'fields': ('is_active',
                                       'is_staff',
                                       'is_superuser',
                                       'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name',
                       'email', 'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
