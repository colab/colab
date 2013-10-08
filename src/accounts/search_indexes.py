# -*- coding: utf-8 -*-

from haystack import indexes

from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr='username')
    name = indexes.CharField(model_attr='get_full_name')
    email = indexes.CharField(model_attr='email')
    institution = indexes.CharField(model_attr='institution', null=True)
    role = indexes.CharField(model_attr='role', null=True)
    twitter = indexes.CharField(model_attr='twitter', null=True)
    facebook = indexes.CharField(model_attr='facebook', null=True)
    google_talk = indexes.CharField(model_attr='google_talk', null=True)
    webpage = indexes.CharField(model_attr='webpage', null=True)

    type = indexes.CharField()

    def get_model(self):
        return User

    def prepare_type(self, obj):
        return u'user'

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True)
