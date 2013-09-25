# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from super_archives.models import MailingList


User = get_user_model()


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
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',
                  'institution', 'role', 'twitter', 'facebook',
                  'google_talk', 'webpage')


class ListsForm(forms.Form):
    LISTS_NAMES = ((list.name, list.name) for list in MailingList.objects.all())
    lists = forms.MultipleChoiceField(label=_(u'Mailing lists'),
                                      required=False,
                                      widget=forms.CheckboxSelectMultiple,
                                      choices=LISTS_NAMES)
