# -*- coding: utf-8 -*-

import math

from datetime import datetime

from django.db.models import Q
from haystack import indexes

from search.base_indexes import BaseIndex
from .models import Ticket, Wiki, Revision


class WikiIndex(BaseIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='name')
    collaborators = indexes.CharField(
        model_attr='collaborators',
        null=True,
        stored=False,
    )

    def get_model(self):
        return Wiki

    def prepare_description(self, obj):
        return u'{}\n{}'.format(obj.wiki_text, obj.collaborators)

    def prepare_icon_name(self, obj):
        return u'file'

    def prepare_type(self, obj):
        return u'wiki'


class TicketIndex(BaseIndex, indexes.Indexable):
    tag = indexes.CharField(model_attr='status', null=True)
    milestone = indexes.CharField(model_attr='milestone', null=True)
    component = indexes.CharField(model_attr='component', null=True)
    severity = indexes.CharField(model_attr='severity', null=True)
    reporter = indexes.CharField(model_attr='reporter', null=True)
    keywords = indexes.CharField(model_attr='keywords', null=True)
    collaborators = indexes.CharField(
        model_attr='collaborators',
        null=True,
        stored=False,
    )

    def get_model(self):
        return Ticket

    def prepare_description(self, obj):
        return u'{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(
            obj.description, obj.milestone, obj.component, obj.severity,
            obj.reporter, obj.keywords, obj.collaborators
        )

    def prepare_icon_name(self, obj):
        return u'tag'

    def prepare_title(self, obj):
        return u'#{} - {}'.format(obj.pk, obj.summary)

    def prepare_type(self, obj):
        return 'ticket'


class RevisionIndex(BaseIndex, indexes.Indexable):
    description = indexes.CharField(model_attr='message', null=True)
    modified = indexes.DateTimeField(model_attr='created', null=True)
    repository_name = indexes.CharField(
        model_attr='repository_name',
        stored=False
    )

    def get_model(self):
        return Revision

    def get_updated_field(self):
        return 'created'

    def get_boost(self, obj, data):
        if obj.hits <= 10:
            data['boost'] = 0.8
        else:
            data['boost'] = math.log(obj.hits) * 0.8

    def prepare_icon_name(self, obj):
        return u'align-right'

    def prepare_title(self, obj):
        return u'{} [{}]'.format(obj.repository_name, obj.rev)

    def prepare_type(self, obj):
        return 'changeset'
