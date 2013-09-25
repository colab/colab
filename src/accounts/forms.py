# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from super_archives.models import MailingList


User = get_user_model()


class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            field.required = True


class ListsForm(forms.Form):
    LISTS_NAMES = ((list.name, list.name) for list in MailingList.objects.all())
    lists = forms.MultipleChoiceField(label=_(u'Mailing lists'),
                                      required=False,
                                      widget=forms.CheckboxSelectMultiple,
                                      choices=LISTS_NAMES)
