# -*- coding: utf-8 -*-

from datetime import datetime

from django.db.models import Q
from haystack import indexes

from .models import Ticket, Wiki, Revision


class WikiIndex(indexes.SearchIndex, indexes.Indexable):
    # common fields
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url')
    title = indexes.CharField(model_attr='name')
    description = indexes.CharField(null=True)
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True)
    created = indexes.DateTimeField(model_attr='created', null=True)
    modified = indexes.DateTimeField(model_attr='modified', null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField()
    author_username = indexes.CharField(null=True)

    # trac extra fields
    collaborators = indexes.CharField(model_attr='collaborators', null=True)

    def get_model(self):
        return Wiki

    def get_updated_field(self):
        return 'modified'

    def prepare_author(self, obj):
        author = obj.get_author()
        if author:
            return author.get_full_name()
        return obj.author

    def prepare_author_username(self, obj):
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
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url')
    title = indexes.CharField()
    description = indexes.CharField(null=True)
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True)
    created = indexes.DateTimeField(model_attr='created', null=True)
    modified = indexes.DateTimeField(model_attr='modified', null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField()
    tag = indexes.CharField(model_attr='status', null=True)
    author_username = indexes.CharField(null=True)

    # trac extra fields
    milestone = indexes.CharField(model_attr='milestone', null=True)
    component = indexes.CharField(model_attr='component', null=True)
    severity = indexes.CharField(model_attr='severity', null=True)
    reporter = indexes.CharField(model_attr='reporter', null=True)
    keywords = indexes.CharField(model_attr='keywords', null=True)
    collaborators = indexes.CharField(model_attr='collaborators', null=True)

    def get_model(self):
        return Ticket

    def get_updated_field(self):
        return 'modified'

    def prepare_author(self, obj):
        author = obj.get_author()
        if author:
            return author.get_full_name()
        return obj.author

    def prepare_author_username(self, obj):
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
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url')
    title = indexes.CharField()
    description = indexes.CharField(model_attr='message', null=True)
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True)
    created = indexes.DateTimeField(model_attr='created', null=True)
    modified = indexes.DateTimeField(model_attr='created', null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField()
    author_username = indexes.CharField(null=True)

    # trac extra fields
    repository_name = indexes.CharField(model_attr='repository_name')
    revision = indexes.CharField(model_attr='rev')

    def get_model(self):
        return Revision

    def get_updated_field(self):
        return 'created'

    def prepare_author(self, obj):
        author = obj.get_author()
        if author:
            return author.get_full_name()
        return obj.author

    def prepare_author_username(self, obj):
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
