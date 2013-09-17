# -*- coding: utf-8 -*-

from django import forms
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
    first_name = forms.CharField(max_length=30, label=_(u'Name'),
                                 widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30, label=_(u'Last name'),
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(validators=[UniqueValidator(User, 'email')],
                             widget=forms.TextInput(attrs={'class':'form-control'}))
    lists = forms.MultipleChoiceField(label=u'Listas',
                                      required=False,
                                      widget=forms.CheckboxSelectMultiple,
                                      choices=LISTS_NAMES)


    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields.pop('password1')
        self.fields.pop('password2')


class UserUpdateForm(UserCreationForm):
    institution= forms.CharField(max_length=120, label=_(u'Institution'), required=False,
                                 widget=forms.TextInput(attrs={'class':'form-control'}))
    role = forms.CharField(max_length=60, label=_(u'Role'), required=False,
                           widget=forms.TextInput(attrs={'class':'form-control'}))
    twitter = forms.URLField(label=_(u'Twitter'), required=False,
                             widget=forms.TextInput(attrs={'class':'form-control'}))
    facebook = forms.URLField(label=_(u'Facebook'), required=False,
                              widget=forms.TextInput(attrs={'class':'form-control'}))
    google_talk = forms.EmailField(label=_(u'Google Talk'), required=False,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    webpage = forms.URLField(label=_(u'Personal Website/Blog'), required=False,
                             widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields.pop('first_name')
        self.fields.pop('last_name')
        self.fields.pop('email')
        self.fields.pop('lists')
