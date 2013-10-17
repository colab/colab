# -*- coding: utf-8 -*-

import unicodedata

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm

from accounts.models import User
from super_archives.models import Message


class ColabSearchForm(SearchForm):
    q = forms.CharField(label=_('Search'), required=False)
    order = forms.CharField(widget=forms.HiddenInput(), required=False)
    type = forms.CharField(required=False, label=_(u'Type'))

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data.get('q'):
            q = unicodedata.normalize(
                'NFKD', unicode(self.cleaned_data.get('q'))
            ).encode('ascii', 'ignore')
            sqs = self.searchqueryset.auto_query(q)
        else:
            sqs = self.searchqueryset.all()

        if self.cleaned_data['type']:
            "It will consider other types with a whitespace"
            types = self.cleaned_data['type']
            sqs = sqs.filter(type__in=types.split())


        if self.cleaned_data['order']:
            for option, dict_order in settings.ORDERING_DATA.items():
                if self.cleaned_data['order'] == option:
                    if dict_order['fields']:
                        sqs = sqs.order_by(*dict_order['fields'])
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


        if self.load_all:
            sqs = sqs.load_all()

        return sqs
