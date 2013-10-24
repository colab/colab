# -*- coding: utf-8 -*-

import math

from datetime import datetime

from django.db.models import Q
from haystack import indexes

from .models import Ticket, Wiki, Revision


class WikiIndex(indexes.SearchIndex, indexes.Indexable):
    # common fields
    text = indexes.CharField(document=True, use_template=True, stored=False)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)
    title = indexes.CharField(model_attr='name')
    description = indexes.CharField(null=True)
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True, indexed=False)
    created = indexes.DateTimeField(model_attr='created', null=True)
    modified = indexes.DateTimeField(model_attr='modified', null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField(indexed=False)
    author_and_username = indexes.CharField(null=True, stored=False)
    hits = indexes.IntegerField()

    # trac extra fields
    collaborators = indexes.CharField(
        model_attr='collaborators',
        null=True,
        stored=False,
    )

    def get_model(self):
        return Wiki

    def get_updated_field(self):
        return 'modified'

    def prepare(self, obj):
        data = super(WikiIndex, self).prepare(obj)
        if obj.hits in [0, 1]:
            data['boost'] = 1
        else:
            data['boost'] = math.log(obj.hits, 2)
        return data

    def prepare_hits(self, obj):
        return obj.hits

    def prepare_author(self, obj):
        author = obj.get_author()
        if author:
            return author.get_full_name()
        return obj.author

    def prepare_author_and_username(self, obj):
        author = obj.get_author()
        if not author:
            return obj.author
        return u'{}\n{}'.format(
            author.get_full_name(),
            author.username,
        )

    def prepare_author_url(self, obj):
        author = obj.get_author()
        if author:
            return author.get_absolute_url()
        return None

    def prepare_description(self, obj):
        return u'{}\n{}'.format(obj.wiki_text, obj.collaborators)

    def prepare_icon_name(self, obj):
        return u'file'

    def prepare_type(self, obj):
        return u'wiki'


class TicketIndex(indexes.SearchIndex, indexes.Indexable):
    # common fields
    text = indexes.CharField(document=True, use_template=True, stored=False)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)
    title = indexes.CharField()
    description = indexes.CharField(null=True)
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True, indexed=False)
    created = indexes.DateTimeField(model_attr='created', null=True)
    modified = indexes.DateTimeField(model_attr='modified', null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField(indexed=False)
    tag = indexes.CharField(model_attr='status', null=True)
    author_and_username = indexes.CharField(null=True, stored=False)
    hits = indexes.IntegerField()

    # trac extra fields
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

    def get_updated_field(self):
        return 'modified'

    def prepare(self, obj):
        data = super(TicketIndex, self).prepare(obj)
        if obj.hits in [0, 1]:
            data['boost'] = 1
        else:
            data['boost'] = math.log(obj.hits, 2)
        return data

    def prepare_hits(self, obj):
        return obj.hits

    def prepare_author(self, obj):
        author = obj.get_author()
        if author:
            return author.get_full_name()
        return obj.author

    def prepare_author_and_username(self, obj):
        author = obj.get_author()
        if not author:
            return obj.author
        return u'{}\n{}'.format(
            author.get_full_name(),
            author.username,
        )

    def prepare_author_url(self, obj):
        author = obj.get_author()
        if author:
            return author.get_absolute_url()
        return None

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


class RevisionIndex(indexes.SearchIndex, indexes.Indexable):
    # common fields
    text = indexes.CharField(document=True, use_template=True, stored=False)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)
    title = indexes.CharField()
    description = indexes.CharField(model_attr='message', null=True)
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True, indexed=False)
    created = indexes.DateTimeField(model_attr='created', null=True)
    modified = indexes.DateTimeField(model_attr='created', null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField(indexed=False)
    author_and_username = indexes.CharField(null=True, stored=False)
    hits = indexes.IntegerField()

    # trac extra fields
    repository_name = indexes.CharField(
        model_attr='repository_name',
        stored=False
    )

    def get_model(self):
        return Revision

    def get_updated_field(self):
        return 'created'

    def prepare(self, obj):
        data = super(RevisionIndex, self).prepare(obj)
        if obj.hits in [0, 1]:
            data['boost'] = 1
        else:
            data['boost'] = math.log(obj.hits, 2)
        return data

    def prepare_hits(self, obj):
        return obj.hits

    def prepare_author(self, obj):
        author = obj.get_author()
        if author:
            return author.get_full_name()
        return obj.author

    def prepare_author_and_username(self, obj):
        author = obj.get_author()
        if not author:
            return obj.author
        return u'{}\n{}'.format(
            author.get_full_name(),
            author.username,
        )

    def prepare_author_url(self, obj):
        author = obj.get_author()
        if author:
            return author.get_absolute_url()
        return None

    def prepare_icon_name(self, obj):
        return u'align-right'

    def prepare_title(self, obj):
        return u'{} [{}]'.format(obj.repository_name, obj.rev)

    def prepare_type(self, obj):
        return 'changeset'
