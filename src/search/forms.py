# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm

from accounts.models import User
from super_archives.models import Message


class ColabSearchForm(SearchForm):
    q = forms.CharField(label=_('Search'))
    type = forms.CharField(required=False, label=_(u'Type'))

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data.get('q'):
            sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])
        else:
            sqs = self.searchqueryset.all()

        if self.cleaned_data['type']:
            sqs = sqs.filter(type=self.cleaned_data['type'])
           # if self.cleaned_data['type'] == 'user':
           #     sqs = self.searchqueryset.models(User)
           # elif self.cleaned_data['type'] in ['message', 'thread']:
           #     sqs = self.searchqueryset.models(Message)
           # elif self.cleaned_data['type'] == 'wiki':
           #     sqs = self.searchqueryset.models(Wiki)
           # elif self.cleaned_data['type'] == 'changeset':
           #     sqs = self.searchqueryset.models(Changeset)
           # elif self.cleaned_data['type'] == 'ticket':
           #     sqs = self.searchqueryset.models(Ticket)
           # else:
           #     sqs = self.searchqueryset.all()
        else:
            sqs = self.searchqueryset.models(User, Message)


        if self.load_all:
            sqs = sqs.load_all()

        return sqs
