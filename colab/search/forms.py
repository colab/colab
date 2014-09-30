# -*- coding: utf-8 -*-

import unicodedata

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm
from haystack.inputs import AltParser

from accounts.models import User
from super_archives.models import Message, MailingList


class ColabSearchForm(SearchForm):
    q = forms.CharField(label=_('Search'), required=False)
    order = forms.CharField(widget=forms.HiddenInput(), required=False)
    type = forms.CharField(required=False, label=_(u'Type'))
    author = forms.CharField(required=False, label=_(u'Author'))
    modified_by = forms.CharField(required=False, label=_(u'Modified by'))
    # ticket status
    tag = forms.CharField(required=False, label=_(u'Status'))
    # mailinglist tag
    list = forms.MultipleChoiceField(
        required=False,
        label=_(u'Mailinglist'),
        choices=[(v, v) for v in MailingList.objects.values_list(
                 'name', flat=True)]
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
    since = forms.DateField(required=False, label=_(u'Since'))
    until = forms.DateField(required=False, label=_(u'Until'))
    filename = forms.CharField(required=False, label=_(u'Filename'))
    used_by = forms.CharField(required=False, label=_(u'Used by'))
    mimetype = forms.CharField(required=False, label=_(u'File type'))
    size = forms.CharField(required=False, label=_(u'Size'))

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        # filter_or goes here
        sqs = self.searchqueryset.all()
        mimetype = self.cleaned_data['mimetype']
        if mimetype:
            filter_mimetypes = {'mimetype__in': []}
            for type_, display, mimelist in settings.FILE_TYPE_GROUPINGS:
                if type_ in mimetype:
                    filter_mimetypes['mimetype__in'] += mimelist
                    if not self.cleaned_data['size']:
                        sqs = sqs.filter_or(mimetype__in=mimelist)

        if self.cleaned_data['size']:
            # (1024 * 1024) / 2
            # (1024 * 1024) * 10
            filter_sizes = {}
            filter_sizes_exp = {}
            if '<500KB' in self.cleaned_data['size']:
                filter_sizes['size__lt'] = 524288
            if '500KB__10MB' in self.cleaned_data['size']:
                filter_sizes_exp['size__gte'] = 524288
                filter_sizes_exp['size__lte'] = 10485760
            if '>10MB' in self.cleaned_data['size']:
                filter_sizes['size__gt'] = 10485760

            if self.cleaned_data['mimetype']:
                # Add the mimetypes filters to this dict and filter it
                if filter_sizes_exp:
                    filter_sizes_exp.update(filter_mimetypes)
                    sqs = sqs.filter_or(**filter_sizes_exp)
                for filter_or in filter_sizes.items():
                    filter_or = dict((filter_or, ))
                    filter_or.update(filter_mimetypes)
                    sqs = sqs.filter_or(**filter_or)
            else:
                for filter_or in filter_sizes.items():
                    filter_or = dict((filter_or, ))
                    sqs = sqs.filter_or(**filter_or)
                sqs = sqs.filter_or(**filter_sizes_exp)

        if self.cleaned_data['used_by']:
            sqs = sqs.filter_or(used_by__in=self.cleaned_data['used_by'].split())


        if self.cleaned_data['q']:
            q = unicodedata.normalize(
                'NFKD', self.cleaned_data.get('q')
            ).encode('ascii', 'ignore')

            dismax_opts = {
                'q.alt': '*.*',
                'pf': 'title^2.1 author^1.9 description^1.7',
                'mm': '2<70%',

                # Date boosting: http://wiki.apache.org/solr/FunctionQuery#Date_Boosting
                'bf': 'recip(ms(NOW/HOUR,modified),3.16e-11,1,1)^10',
            }

            sqs = sqs.filter(content=AltParser('edismax', q, **dismax_opts))

        if self.cleaned_data['type']:
            sqs = sqs.filter(type=self.cleaned_data['type'])

        if self.cleaned_data['order']:
            for option, dict_order in settings.ORDERING_DATA.items():
                if self.cleaned_data['order'] == option:
                    if dict_order['fields']:
                        sqs = sqs.order_by(*dict_order['fields'])

        if self.cleaned_data['author']:
            sqs = sqs.filter(
                fullname_and_username__contains=self.cleaned_data['author']
            )

        if self.cleaned_data['modified_by']:
            sqs = sqs.filter(
                fullname_and_username__contains=self.cleaned_data['modified_by']
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

        if self.cleaned_data['since']:
            sqs = sqs.filter(modified__gte=self.cleaned_data['since'])
        if self.cleaned_data['until']:
            sqs = sqs.filter(modified__lte=self.cleaned_data['until'])

        if self.cleaned_data['filename']:
            sqs = sqs.filter(filename=self.cleaned_data['filename'])

        return sqs
