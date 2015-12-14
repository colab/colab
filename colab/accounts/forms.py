# -*- coding: utf-8 -*-

from importlib import import_module

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (ReadOnlyPasswordHashField,
                                       SetPasswordForm, PasswordChangeForm)
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from .signals import user_created
from .utils.validators import validate_social_account
from .utils import mailman

User = get_user_model()

SOCIAL_NETWORK_ENABLED = getattr(settings, 'SOCIAL_NETWORK_ENABLED')


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
    username = forms.CharField(
        # Forces username to be lowercase always
        widget=forms.TextInput(attrs={'style': 'text-transform: lowercase;'}),
    )
    required = ('first_name', 'last_name', 'username')

    class Meta:
        fields = ('first_name', 'last_name', 'username')
        model = User

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Adds form-control class to all form fields
            field.widget.attrs.update({'class': 'form-control'})

            # Set UserForm.required fields as required
            if field_name in UserForm.required:
                field.required = True

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if not username:
            raise forms.ValidationError(_('This field cannot be blank.'))
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].strip()
        if not first_name:
            raise forms.ValidationError(_('This field cannot be blank.'))
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].strip()
        if not last_name:
            raise forms.ValidationError(_('This field cannot be blank.'))
        return last_name

    def clean_twitter(self):
        twitter = self.cleaned_data["twitter"]
        if twitter is not None and twitter.isspace():
                return self.initial.get("twitter")
        return twitter

    def clean_facebook(self):
        facebook = self.cleaned_data["facebook"]
        if facebook is not None and facebook.isspace():
                return self.initial.get("facebook")
        return facebook

    def clean_webpage(self):
        webpage = self.cleaned_data["webpage"].strip()
        return webpage

    def clean_role(self):
        role = self.cleaned_data["role"].strip()
        return role

    def clean_institution(self):
        institution = self.cleaned_data["institution"].strip()
        return institution

    def clean_bio(self):
        bio = self.cleaned_data["bio"].strip()
        return bio

    def clean_github(self):
        github = self.cleaned_data["github"].strip()
        return github


class UserUpdateForm(UserForm):

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '6', 'maxlength': '200'}),
        max_length=200,
        label=_(u'Bio'),
        help_text=_(u'Write something about you in 200 characters or less.'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'institution', 'role')
        if SOCIAL_NETWORK_ENABLED:
            fields += ('twitter', 'facebook', 'google_talk', 'github')
        fields += ('webpage', 'bio')

    if SOCIAL_NETWORK_ENABLED:
        twitter = SocialAccountField(url='https://twitter.com/',
                                     required=False)
        facebook = SocialAccountField(url='https://graph.facebook.com/',
                                      required=False)


def get_lists_choices():
    lists_names = []
    for mlist in mailman.all_lists():
        name = mlist.get('listname')
        desc = mlist.get('description')
        formatted_desc = u'{} ({})'.format(name, desc)
        lists_names.append((name, formatted_desc))
    return lists_names


# XXX: This field is no longer required when using django 1.8
class MultipleChoiceFieldLazy(forms.MultipleChoiceField):
    def _set_choices(self, value):
        self._choices = self.widget.choices = value

    def _get_choices(self):
        return list(self._choices)

    choices = property(_get_choices, _set_choices)


class ListsForm(forms.Form):
    lists = MultipleChoiceFieldLazy(label=_(u'Mailing lists'),
                                    required=False,
                                    widget=forms.CheckboxSelectMultiple,
                                    choices=lazy(get_lists_choices, list)())


class CustomValidator(object):

    def apply_custom_validators(self, validator_type, validator_field):
        for app in settings.COLAB_APPS.values():
            if validator_type in app:
                for validator_path in app.get(validator_type):
                    module_path, func_name = validator_path.rsplit('.', 1)
                    module = import_module(module_path)
                    validator_func = getattr(module, func_name, None)
                    if validator_func:
                        validator_func(validator_field)

        return validator_field


class ColabSetUsernameFormMixin(CustomValidator):

    def clean_username(self):
        try:
            username = super(ColabSetUsernameFormMixin,
                             self).clean_username()
        except AttributeError:
            username = self.cleaned_data['username']

        self.apply_custom_validators('username_validators', username)
        return username


class ColabSetPasswordFormMixin(CustomValidator):

    def clean_new_password2(self):
        try:
            password = super(ColabSetPasswordFormMixin,
                             self).clean_new_password2()
        except AttributeError:
            password = self.cleaned_data['new_password2']

        self.apply_custom_validators('password_validators', password)
        return password

    def clean_password2(self):
        try:
            password = super(ColabSetPasswordFormMixin, self).clean_password2()
        except AttributeError:
            password = self.cleaned_data['password2']

        self.apply_custom_validators('password_validators', password)
        return password


class UserCreationForm(UserForm, ColabSetPasswordFormMixin):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    error_messages = {
        'duplicate_email': _("Email already used. Is it you? "
                             " Please <a href='%(url)s'>login</a>"),
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
                                regex=r'^[\w]+$',
                                help_text=_(("Required. 30 characters or fewer"
                                             ". Letter and digits.")),
                                error_messages={
                                    'invalid': _(("This value may contain only"
                                                  " letters and numbers."))})

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_(("Enter the same password as above"
                                             ", for verification.")))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        user_qs = User.objects.filter(email=email).exclude(username=username)

        if email and user_qs.exists():
            msg = self.error_messages.get('duplicate_email') % {
                'url': reverse('login')
            }

            raise forms.ValidationError(mark_safe(msg))

        return email

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"].strip()
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        super(UserCreationForm, self).clean_password2()
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        password = self.cleaned_data["password1"]
        user.set_password(password)

        if commit:
            user.save()

        user_created.send(user.__class__, user=user, password=password)

        return user


class UserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r'^[\w]+$',
        help_text=_("Required. 30 characters or fewer. Letters and digits."),
        error_messages={
            'invalid': _("This value may contain only letters and numbers.")})
    # TODO: remove this hardcoded URL from here
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not"
                                                     " stored, so there is no"
                                                     " way to see "
                                                     "this user's password, "
                                                     "but you can change the "
                                                     "password "
                                                     "using <a "
                                                     "href=\"password/\">this"
                                                     " form</a>."))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

        # Set email as required field
        self.fields['email'].required = True

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ColabSetPasswordForm(ColabSetPasswordFormMixin, SetPasswordForm):
    pass


class ColabPasswordChangeForm(ColabSetPasswordFormMixin, PasswordChangeForm):
    pass


class ColabSetUsernameForm(ColabSetUsernameFormMixin, UserCreationForm):
    pass
