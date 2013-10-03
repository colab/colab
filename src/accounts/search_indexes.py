# -*- coding: utf-8 -*-

from haystack import indexes

from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr='username')
    name = indexes.CharField(model_attr='get_full_name')
    email = indexes.CharField(model_attr='email')
    institution = indexes.CharField(model_attr='institution')
    role = indexes.CharField(model_attr='role')
    twitter = indexes.CharField(model_attr='twitter')
    facebook = indexes.CharField(model_attr='facebook')
    google_talk = indexes.CharField(model_attr='google_talk')
    webpage = indexes.CharField(model_attr='webpage')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True)
