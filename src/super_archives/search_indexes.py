# -*- coding: utf-8 -*-

from haystack import indexes

from .models import Thread


class ThreadIndex(indexes.SearchIndex, indexes.Indexable):
    # common fields
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url', null=True)
    title = indexes.CharField(model_attr='latest_message__subject_clean')
    description = indexes.CharField(use_template=True)
    created = indexes.DateTimeField()
    modified = indexes.DateTimeField(
        model_attr='latest_message__received_time'
    )
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField()
    tag = indexes.CharField(model_attr='mailinglist__name')

    mailinglist_url = indexes.CharField(
        model_attr='mailinglist__get_absolute_url'
    )

    def get_model(self):
        return Thread

    def get_updated_field(self):
        return 'latest_message__received_time'

    def prepare_author(self, obj):
        return obj.message_set.first().from_address.get_full_name()

    def prepare_author_url(self, obj):
        first_message = obj.message_set.first()
        if first_message.from_address.user:
            return first_message.from_address.user.get_absolute_url()
        return None

    def prepare_created(self, obj):
        return obj.message_set.first().received_time

    def prepare_icon_name(self, obj):
        return u'envelope'

    def prepare_type(self, obj):
        return u'thread'

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            spam=False
        ).exclude(subject_token='')
