# -*- coding: utf-8 -*-

from collections import OrderedDict

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.functional import lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


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


class UserCreationForm(UserForm):
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
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
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


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(
            UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(
                self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.
        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.
        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)

            if html_email_template_name:
                html_email = loader.render_to_string(html_email_template_name,
                                                     c)
            else:
                html_email = None
            send_mail(subject, email, from_email, [user.email],
                      html_message=html_email)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)


class AdminPasswordChangeForm(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (again)"),
                                widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AdminPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        """
        Saves the new password.
        """
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        return self.user

    def _get_changed_data(self):
        data = super(AdminPasswordChangeForm, self).changed_data
        for name in self.fields.keys():
            if name not in data:
                return []
        return ['password']
