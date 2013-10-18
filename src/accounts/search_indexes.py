# -*- coding: utf-8 -*-

from haystack import indexes

from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    # common fields
    text = indexes.CharField(document=True, use_template=True)
    url = indexes.CharField(model_attr='get_absolute_url')
    title = indexes.CharField(model_attr='get_full_name')
    description = indexes.CharField(null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField()

    # extra fields
    username = indexes.CharField(model_attr='username')
    name = indexes.CharField(model_attr='get_full_name')
    email = indexes.CharField(model_attr='email')
    institution = indexes.CharField(model_attr='institution', null=True)
    role = indexes.CharField(model_attr='role', null=True)
    google_talk = indexes.CharField(model_attr='google_talk', null=True)
    webpage = indexes.CharField(model_attr='webpage', null=True)

    def get_model(self):
        return User

    def get_updated_field(self):
        return 'date_joined'

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
