# -*- coding: utf-8 -*-

import unicodedata

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm
from haystack.inputs import AltParser
from haystack.inputs import AutoQuery

from colab.plugins.utils import filters_importer


class ColabSearchForm(SearchForm):
    q = forms.CharField(label=_('Search'), required=False)
    order = forms.CharField(widget=forms.HiddenInput(), required=False)
    type = forms.CharField(required=False, label=_(u'Type'))
    since = forms.DateField(required=False, label=_(u'Since'))
    until = forms.DateField(required=False, label=_(u'Until'))

    excluded_fields = []

    def __init__(self, *args, **kwargs):
        super(ColabSearchForm, self).__init__(*args, **kwargs)
        extra = filters_importer.import_plugin_filters({})
        for filter_types in extra.values():
            for field in filter_types['fields']:
                self.fields[field[0]] = forms.CharField(required=False,
                                                        label=field[1])

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        # filter_or goes here
        sqs = self.searchqueryset.all()

        kwargs = {}

        self.excluded_fields.extend(['q', 'type', 'since', 'until', 'order'])

        if self.cleaned_data['type']:
            all_types = self.cleaned_data['type'].split(' ')
            sqs = sqs.filter_or(type__in=all_types)

        for key in self.fields.keys():
            value = self.cleaned_data[key]
            if value and key not in self.excluded_fields:
                kwargs[key] = self.cleaned_data[key]

        sqs = sqs.filter(**kwargs)

        if self.cleaned_data['q']:
            q = unicodedata.normalize(
                'NFKD', self.cleaned_data.get('q')
            ).encode('ascii', 'ignore')

            dismax_opts = {
                'q.alt': '*.*',
                'pf': 'title^2.1 author^1.9 description^1.7',
                'mm': '2<70%',

                # Date boosting:
                # http://wiki.apache.org/solr/FunctionQuery#Date_Boosting
                'bf': 'recip(ms(NOW/HOUR,modified),3.16e-11,1,1)^10',
            }
            hayString = 'haystack.backends.whoosh_backend.WhooshEngine'
            if settings.HAYSTACK_CONNECTIONS['default']['ENGINE'] != hayString:
                        sqs = sqs.filter(content=AltParser(
                                         'edismax', q, **dismax_opts))

            else:
                sqs = sqs.filter(content=AutoQuery(q))

        if self.cleaned_data['order']:
            for option, dict_order in settings.ORDERING_DATA.items():
                if self.cleaned_data['order'] == option:
                    if dict_order['fields']:
                        sqs = sqs.order_by(*dict_order['fields'])

        if self.cleaned_data['since']:
            sqs = sqs.filter(modified__gte=self.cleaned_data['since'])
        if self.cleaned_data['until']:
            sqs = sqs.filter(modified__lte=self.cleaned_data['until'])

        return sqs
