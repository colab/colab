# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from conversejs.models import XMPPAccount

from accounts.utils import mailman
from super_archives.models import MailingList
from .utils.validators import validate_social_account

User = get_user_model()


class SocialAccountField(forms.Field):
    def __init__(self, *args, **kwargs):
        self.url = kwargs.pop('url', None)
        super(SocialAccountField, self).__init__(*args, **kwargs)

    def validate(self, value):
        super(SocialAccountField, self).validate(value)

        if value and not validate_social_account(value, self.url):
            raise forms.ValidationError(_('Social account does not exist'),
                                        code='social-account-doesnot-exist')


class UserForm(forms.ModelForm):
    required = ('first_name', 'last_name', 'email', 'username')

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Adds form-control class to all form fields
            field.widget.attrs.update({'class': 'form-control'})

            # Set UserForm.required fields as required
            if field_name in UserForm.required:
                field.required = True


class UserCreationForm(UserForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class UserUpdateForm(UserForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '6', 'maxlength': '200'}),
        max_length=200,
        label=_(u'Bio'),
        help_text=_(u'Write something about you in 200 characters or less.'),
        required=False,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'institution', 'role', 'twitter', 'facebook',
                  'google_talk', 'github', 'webpage', 'bio')

    twitter = SocialAccountField(url='https://twitter.com/', required=False)
    facebook = SocialAccountField(url='https://graph.facebook.com/', required=False)


class ListsForm(forms.Form):
    LISTS_NAMES = ((
        listname, u'{} ({})'.format(listname, description)
    ) for listname, description in mailman.all_lists(description=True))

    lists = forms.MultipleChoiceField(label=_(u'Mailing lists'),
                                      required=False,
                                      widget=forms.CheckboxSelectMultiple,
                                      choices=LISTS_NAMES)


class ChangeXMPPPasswordForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = XMPPAccount
        fields = ('password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ChangeXMPPPasswordForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Adds form-control class to all form fields
            field.widget.attrs.update({'class': 'form-control'})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("Password mismatch"),
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        self.instance.password = self.cleaned_data['password2']
        if commit:
            self.instance.save()
        return self.instance
