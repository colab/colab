# -*- coding: utf-8 -*-

from haystack import indexes

from .models import Thread


class ThreadIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    subject_token = indexes.CharField(model_attr='subject_token')
    mailinglist = indexes.CharField(model_attr='mailinglist')
    latest_message = indexes.CharField(model_attr='latest_message')
    Description = indexes.CharField(use_template=True)
    Title = indexes.CharField(use_template=True)
    url = indexes.CharField(use_template=True, null=True)
    modified = indexes.DateTimeField(use_template=True)

    def get_model(self):
        return Thread

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(spam=False)
