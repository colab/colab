# -*- coding: utf-8 -*-

import math

from haystack import indexes

from .models import Thread


class ThreadIndex(indexes.SearchIndex, indexes.Indexable):
    # common fields
    text = indexes.CharField(document=True, use_template=True, stored=False)
    url = indexes.CharField(
        model_attr='get_absolute_url',
        null=True,
        indexed=False
    )
    title = indexes.CharField(model_attr='latest_message__subject_clean')
    description = indexes.CharField(use_template=True)
    latest_description = indexes.CharField(
        model_attr='latest_message__body',
        indexed=False,
    )
    created = indexes.DateTimeField()
    modified = indexes.DateTimeField(
        model_attr='latest_message__received_time'
    )
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True, indexed=False)
    type = indexes.CharField()
    icon_name = indexes.CharField(indexed=False)
    tag = indexes.CharField(model_attr='mailinglist__name')
    collaborators = indexes.CharField(use_template=True, stored=False)

    author_and_username = indexes.CharField(null=True, stored=False)
    mailinglist_url = indexes.CharField(
        model_attr='mailinglist__get_absolute_url',
        indexed=False,
    )
    hits = indexes.IntegerField()

    def get_model(self):
        return Thread

    def get_updated_field(self):
        return 'latest_message__received_time'

    def prepare(self, obj):
        data = super(ThreadIndex, self).prepare(obj)
        if obj.hits <= 10:
            data['boost'] = 1
        else:
            data['boost'] = math.log(obj.hits)
        return data

    def prepare_hits(self, obj):
        return obj.hits

    def prepare_author(self, obj):
        return obj.message_set.first().from_address.get_full_name()

    def prepare_author_and_username(self, obj):
        from_address = obj.message_set.first().from_address
        if not from_address.user:
            return from_address.get_full_name()

        return u'{}\n{}'.format(
            from_address.get_full_name(),
            from_address.user.username,
        )

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
