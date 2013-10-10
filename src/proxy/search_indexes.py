# -*- coding: utf-8 -*-

from datetime import datetime

from django.db.models import Q
from haystack import indexes

from .models import Ticket, Wiki, Revision


class WikiIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    wiki_text = indexes.CharField(model_attr='wiki_text')
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True)
    collaborators = indexes.CharField(model_attr='collaborators', null=True)
    created = indexes.DateTimeField(model_attr='created', null=True)
    modified = indexes.DateTimeField(model_attr='modified', null=True)

    url = indexes.CharField(model_attr='get_absolute_url')
    type = indexes.CharField()

    def get_model(self):
        return Wiki

    def get_updated_field(self):
        return 'modified'

    def prepare_author(self, obj):
        author = obj.get_author()
        if author:
            return author.get_full_name()
        return obj.author

    def prepare_author_url(self, obj):
        author = obj.get_author()
        if author:
            return author.get_absolute_url()
        return None

    def prepare_type(self, obj):
        return u'wiki'


class TicketIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    summary = indexes.CharField(model_attr='summary', null=True)
    description = indexes.CharField(model_attr='description', null=True)
    milestone = indexes.CharField(model_attr='milestone', null=True)
    component = indexes.CharField(model_attr='component', null=True)
    version = indexes.CharField(model_attr='version', null=True)
    severity = indexes.CharField(model_attr='severity', null=True)
    reporter = indexes.CharField(model_attr='reporter', null=True)
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True)
    status = indexes.CharField(model_attr='status', null=True)
    keywords = indexes.CharField(model_attr='keywords', null=True)
    collaborators = indexes.CharField(model_attr='collaborators', null=True)
    created = indexes.DateTimeField(model_attr='created', null=True)
    modified = indexes.DateTimeField(model_attr='modified', null=True)

    url = indexes.CharField(model_attr='get_absolute_url')
    type = indexes.CharField()

    def get_model(self):
        return Ticket

    def get_updated_field(self):
        return 'modified'

    def prepare_author(self, obj):
        author = obj.get_author()
        if author:
            return author.get_full_name()
        return obj.author

    def prepare_author_url(self, obj):
        author = obj.get_author()
        if author:
            return author.get_absolute_url()
        return None

    def prepare_type(self, obj):
        return 'ticket'


class RevisionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    repository_name = indexes.CharField(model_attr='repository_name')
    revision = indexes.CharField(model_attr='rev')
    created = indexes.DateTimeField(model_attr='created', null=True)
    modified = indexes.DateTimeField(model_attr='created', null=True)
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True)
    message = indexes.CharField(model_attr='message', null=True)

    url = indexes.CharField(model_attr='get_absolute_url')
    type = indexes.CharField()

    def get_model(self):
        return Revision

    def get_updated_field(self):
        return 'created'

    def prepare_author(self, obj):
        author = obj.get_author()
        if author:
            return author.get_full_name()
        return obj.author

    def prepare_author_url(self, obj):
        author = obj.get_author()
        if author:
            return author.get_absolute_url()
        return None

    def prepare_type(self, obj):
        return 'changeset'
