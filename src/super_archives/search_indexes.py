# -*- coding: utf-8 -*-

from haystack import indexes

from .models import Message


class MessageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    mailinglist = indexes.CharField(model_attr='thread__mailinglist__name')
    description = indexes.CharField(model_attr='body')
    title = indexes.CharField(model_attr='subject_clean')
    modified = indexes.DateTimeField(model_attr='received_time')
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True)
    url = indexes.CharField(model_attr='url', null=True)

    type = indexes.CharField()

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

    def prepare_type(self, obj):
        return u'thread'

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            thread__spam=False, spam=False
        ).exclude(thread__subject_token='')
