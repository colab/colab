
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
	fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active',
                  'is_staff', 'is_superuser', 'groups', 'last_login',
                  'date_joined', 'twitter', 'facebook', 'google_talk',
		  'webpage')

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True



class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',
				      'twitter', 'facebook', 'google_talk',
                                      'webpage')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
	('Important Dates', {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email')}
        ),
    )


admin.site.register(User, MyUserAdmin)
