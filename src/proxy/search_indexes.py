# -*- coding: utf-8 -*-

from datetime import datetime
from django.db.models import Q
from haystack import indexes

from .models import Wiki


class WikiIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    wiki_text = indexes.CharField(model_attr='text')
    name = indexes.CharField(model_attr='name')
    author = indexes.CharField(model_attr='get_author', null=True)
    collaborators = indexes.CharField(
        model_attr='get_collaborators', null=True
    )
    comment = indexes.CharField(model_attr='comment', null=True)
    time = indexes.DateTimeField(model_attr='time', null=True)

    url = indexes.CharField()
    type = indexes.CharField()

    def get_model(self):
        return Wiki

    def prepare_time(self, obj):
        return datetime.fromtimestamp(self.prepared_data['time']/1000000)

    def prepare_type(self, obj):
        return u'wiki'

    def prepare_url(self, obj):
        return u'/wiki/{}'.format(obj.name)

    def index_queryset(self, using=None):
        wiki = self.get_model().objects.raw(
            '''
            SELECT "wiki"."name", MAX("wiki"."version") AS version
            FROM "wiki"
            GROUP BY "wiki"."name"
            '''
        )

        q = Q()
        for obj in wiki:
            q |= Q(name=obj.name, version=obj.version)

        return self.get_model().objects.filter(q)


# def TicketIndex(indexes.SearchIndex, indexes.Indexable):
#     text =  = indexes.CharField(document=True, use_template=True)
#     time = indexes.CharField(
#     changetime = indexes.CharField(
#     component = indexes.CharField(
#     severity = indexes.CharField(
#     priority = indexes.CharField(
#     owner = indexes.CharField(
#     reporter = indexes.CharField(
#     cc = indexes.CharField(
#     version = indexes.CharField(
#     milestone = indexes.CharField(
#     status = indexes.CharField(
#     resolution = indexes.CharField(
#     summary = indexes.CharField(
#     description = indexes.CharField(
#     keywords = indexes.CharField(
