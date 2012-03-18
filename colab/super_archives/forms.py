# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as UserCreationForm_

from colab.super_archives.models import MailingList
from colab.super_archives.validators import UniqueValidator    

# XXX: I know that this code does not look nice AT ALL.
#   probably it should be implemented using formsets instead of 
#   the hack below. Feel free to improve it! :)

# User fields
username_field = UserCreationForm_().fields.get('username')
first_name_field = forms.CharField(max_length=30, label='Nome')
last_name_field = forms.CharField(max_length=30, label='Sobrenome')
email_field = forms.EmailField(validators=[UniqueValidator(User, 'email')])

# UserProfile fields
institution_field = forms.CharField(max_length=120, label=u'Instituição', 
                                    required=False)
role_field = forms.CharField(max_length=60, label='Função', required=False)
twitter_field = forms.URLField(label=u'Twitter', required=False)
facebook_field = forms.URLField(label=u'Facebook', required=False)
google_talk_field = forms.EmailField(label=u'Google Talk', required=False)
webpage_field = forms.URLField(label=u'Página Pessoal/Blog', required=False)

all_lists = MailingList.objects.all()
lists_names = []
for list_ in all_lists:
   choice = (list_.name, list_.name)
   lists_names.append(choice)

lists_field = forms.MultipleChoiceField(
    label=u'Listas',
    required=False, 
    widget=forms.CheckboxSelectMultiple,
    choices=lists_names
)


class UserCreationForm(UserCreationForm_):
    first_name = first_name_field
    last_name = last_name_field
    email = email_field
    institution = institution_field
    role = role_field
    twitter = twitter_field
    facebook = facebook_field
    google_talk = google_talk_field
    webpage = webpage_field
    lists = lists_field

    
class UserUpdateForm(forms.Form):
    username = username_field
    username.required = False
    institution = institution_field
    role = role_field
    twitter = twitter_field
    facebook = facebook_field
    google_talk = google_talk_field
    webpage = webpage_field
