# -*- coding: utf-8 -*-

from haystack import indexes

from .models import Message


class MessageIndex(indexes.SearchIndex, indexes.Indexable):
    # common fields
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(null=True)
    title = indexes.CharField(model_attr='subject_clean')
    description = indexes.CharField(model_attr='body')
    modified = indexes.DateTimeField(model_attr='received_time')
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField()
    tag = indexes.CharField(model_attr='thread__mailinglist__name')

    mailinglist_url = indexes.CharField(
        model_attr='thread__mailinglist__get_absolute_url'
    )

    def get_model(self):
        return Message

    def get_updated_field(self):
        return 'received_time'

    def prepare_author(self, obj):
        if obj.from_address.user:
            return obj.from_address.user.get_full_name()
        elif obj.from_address.get_full_name():
            return obj.from_address.get_full_name()
        return obj.from_address.real_name

    def prepare_author_url(self, obj):
        if obj.from_address.user:
            return obj.from_address.user.get_absolute_url()
        return None

    def prepare_icon_name(self, obj):
        return u'envelope'

    def prepare_type(self, obj):
        return u'thread'

    def prepare_url(self, obj):
        return u'{}#msg-{}'.format(obj.url, obj.pk)

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            thread__spam=False, spam=False
        ).exclude(thread__subject_token='')
