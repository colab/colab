# -*- coding: utf-8 -*-

import math

from haystack import indexes


class BaseIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True, stored=False)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)
    title = indexes.CharField()
    description = indexes.CharField(null=True)
    fullname = indexes.CharField(null=True)
    author = indexes.CharField(null=True)
    author_url = indexes.CharField(null=True, indexed=False)
    created = indexes.DateTimeField(model_attr='created', null=True)
    modified = indexes.DateTimeField(model_attr='modified', null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField(indexed=False)
    fullname_and_username = indexes.CharField(null=True, stored=False)
    hits = indexes.IntegerField(model_attr='hits')
    modified_by = indexes.CharField(null=True)
    modified_by_url = indexes.CharField(null=True)

    def get_updated_field(self):
        return 'modified'

    def get_boost(self, obj):
        if obj.hits <= 10:
            return 1

        return math.log(obj.hits)

    def prepare(self, obj):
        self.author_obj = None
        if hasattr(obj, 'get_author'):
            self.author_obj = obj.get_author()

        data = super(BaseIndex, self).prepare(obj)
        data['boost'] = self.get_boost(obj)

        return data

    def prepare_author(self, obj):
        if self.author_obj:
            return self.author_obj.username
        return obj.author

    def prepare_author_url(self, obj):
        if self.author_obj:
            return self.author_obj.get_absolute_url()
        return None

    def prepare_fullname(self, obj):
        if hasattr(obj, 'modified_by'):
            modified_by = obj.get_modified_by()
            if modified_by:
                return modified_by.get_full_name()
        if self.author_obj:
            return self.author_obj.get_full_name()
        return obj.author

    def prepare_fullname_and_username(self, obj):
        if hasattr(obj, 'modified_by'):
            modified_by = obj.get_modified_by()
            if modified_by:
                return u'{}\n{}'.format(
                    modified_by.get_full_name(),
                    modified_by.username,
                )
        if not self.author_obj:
            return obj.author
        return u'{}\n{}'.format(
            self.author_obj.get_full_name(),
            self.author_obj.username,
        )

    def prepare_modified_by(self, obj):
        return self.prepare_fullname(obj)

    def prepare_modified_by_url(self, obj):
        if hasattr(obj, 'modified_by'):
            modified_by = obj.get_modified_by()
            if modified_by:
                return modified_by.get_absolute_url()
        if self.author_obj:
            return self.author_obj.get_absolute_url()
        return None
