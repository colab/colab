# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as UserCreationForm_
from django.utils.translation import ugettext_lazy as _

from super_archives.models import MailingList
from super_archives.validators import UniqueValidator


LISTS_NAMES = []
for list_ in MailingList.objects.iterator():
   choice = (list_.name, list_.name)
   LISTS_NAMES.append(choice)


class UserCreationForm(UserCreationForm_):
    first_name = forms.CharField(max_length=30, label=_(u'Name'))
    last_name = forms.CharField(max_length=30, label=_(u'Last name'))
    email = forms.EmailField(validators=[UniqueValidator(User, 'email')])
    institution= forms.CharField(max_length=120, label=_(u'Institution'), required=False)
    role = forms.CharField(max_length=60, label=_(u'Role'), required=False)
    twitter = forms.URLField(label=_(u'Twitter'), required=False)
    facebook = forms.URLField(label=_(u'Facebook'), required=False)
    google_talk = forms.EmailField(label=_(u'Google Talk'), required=False)
    webpage = forms.URLField(label=_(u'Personal Website/Blog'), required=False)
    lists = forms.MultipleChoiceField(label=u'Listas',
                                      required=False,
                                      widget=forms.CheckboxSelectMultiple,
                                      choices=LISTS_NAMES)


    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password1')
        self.fields.pop('password2')


class UserUpdateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields.pop('first_name')
        self.fields.pop('last_name')
        self.fields.pop('email')
        self.fields.pop('lists')
