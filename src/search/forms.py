# -*- coding: utf-8 -*-

import unicodedata

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm

from accounts.models import User
from super_archives.models import Message, MailingList


class ColabSearchForm(SearchForm):
    q = forms.CharField(label=_('Search'), required=False)
    order = forms.CharField(widget=forms.HiddenInput(), required=False)
    type = forms.CharField(required=False, label=_(u'Type'))
    author = forms.CharField(required=False, label=_(u'Author'))
    # ticket status
    tag = forms.CharField(required=False, label=_(u'Status'))
    # mailinglist tag
    list = forms.MultipleChoiceField(
        required=False,
        label=_(u'Mailinglist'),
        choices=[(v, v) for v in MailingList.objects.values('name')
                 for (v, v) in v.items()]
    )
    milestone = forms.CharField(required=False, label=_(u'Milestone'))
    priority = forms.CharField(required=False, label=_(u'Priority'))
    component = forms.CharField(required=False, label=_(u'Component'))
    severity = forms.CharField(required=False, label=_(u'Severity'))
    reporter = forms.CharField(required=False, label=_(u'Reporter'))
    keywords = forms.CharField(required=False, label=_(u'Keywords'))
    collaborators = forms.CharField(required=False, label=_(u'Collaborators'))
    repository_name = forms.CharField(required=False, label=_(u'Repository'))
    username = forms.CharField(required=False, label=_(u'Username'))
    name = forms.CharField(required=False, label=_(u'Name'))
    institution = forms.CharField(required=False, label=_(u'Institution'))
    role = forms.CharField(required=False, label=_(u'Role'))

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

        if self.cleaned_data['author']:
            sqs = sqs.filter(
                author_and_username__contains=self.cleaned_data['author']
            )

        if self.cleaned_data['milestone']:
            sqs = sqs.filter(milestone=self.cleaned_data['milestone'])
        if self.cleaned_data['priority']:
            sqs = sqs.filter(priority=self.cleaned_data['priority'])
        if self.cleaned_data['severity']:
            sqs = sqs.filter(severity=self.cleaned_data['severity'])
        if self.cleaned_data['reporter']:
            sqs = sqs.filter(reporter=self.cleaned_data['reporter'])
        if self.cleaned_data['keywords']:
            sqs = sqs.filter(keywords=self.cleaned_data['keywords'])
        if self.cleaned_data['collaborators']:
            sqs = sqs.filter(collaborators=self.cleaned_data['collaborators'])
        if self.cleaned_data['repository_name']:
            sqs = sqs.filter(
                repository_name=self.cleaned_data['repository_name']
            )
        if self.cleaned_data['username']:
            sqs = sqs.filter(username=self.cleaned_data['username'])
        if self.cleaned_data['name']:
            sqs = sqs.filter(name=self.cleaned_data['name'])
        if self.cleaned_data['institution']:
            sqs = sqs.filter(institution=self.cleaned_data['institution'])
        if self.cleaned_data['role']:
            sqs = sqs.filter(role=self.cleaned_data['role'])
        if self.cleaned_data['tag']:
            sqs = sqs.filter(tag=self.cleaned_data['tag'])

        if self.cleaned_data['list']:
            sqs = sqs.filter(tag__in=self.cleaned_data['list'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
