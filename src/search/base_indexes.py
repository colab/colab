# -*- coding: utf-8 -*-

import math

from haystack import indexes


class BaseIndex(indexes.SearchIndex):
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
    author_and_username = indexes.CharField(null=True, stored=False)
    hits = indexes.IntegerField(model_attr='hits')

    def get_updated_field(self):
        return 'modified'

    def get_boost(self, obj, data):
        if obj.hits <= 10:
            data['boost'] = 1
        else:
            data['boost'] = math.log(obj.hits)

    def prepare(self, obj):
        data = super(BaseIndex, self).prepare(obj)
        self.get_boost(obj, data)
        return data

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
