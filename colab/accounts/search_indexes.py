# -*- coding: utf-8 -*-

from haystack import indexes
from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    # common fields
    text = indexes.EdgeNgramField(document=True, use_template=True, stored=False)
    url = indexes.EdgeNgramField(model_attr='get_absolute_url', indexed=False)
    title = indexes.EdgeNgramField(model_attr='get_full_name')
    description = indexes.EdgeNgramField(null=True)
    type = indexes.EdgeNgramField()
    icon_name = indexes.EdgeNgramField()

    # extra fields
    username = indexes.EdgeNgramField(model_attr='username', stored=False)
    name = indexes.EdgeNgramField(model_attr='get_full_name')
    email = indexes.EdgeNgramField(model_attr='email', stored=False)
    institution = indexes.EdgeNgramField(model_attr='institution', null=True)
    role = indexes.EdgeNgramField(model_attr='role', null=True)
    google_talk = indexes.EdgeNgramField(model_attr='google_talk', null=True,
                                    stored=False)
    webpage = indexes.EdgeNgramField(model_attr='webpage', null=True, stored=False)
    date_joined = indexes.DateTimeField(model_attr='date_joined')

    def get_model(self):
        return User

    def prepare(self, obj):
        prepared_data = super(UserIndex, self).prepare(obj)

        return prepared_data

    def prepare_description(self, obj):
        return u'{}\n{}\n{}\n{}'.format(
            obj.institution, obj.role, obj.username, obj.get_full_name()
        )

    def prepare_icon_name(self, obj):
        return u'user'

    def prepare_type(self, obj):
        return u'user'

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True)
