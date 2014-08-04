# -*- coding: utf-8 -*-

from haystack import indexes
from django.db.models import Count

from proxy.models import Revision, Ticket, Wiki
from badger.utils import get_users_counters
from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    # common fields
    text = indexes.CharField(document=True, use_template=True, stored=False)
    url = indexes.CharField(model_attr='get_absolute_url', indexed=False)
    title = indexes.CharField(model_attr='get_full_name')
    description = indexes.CharField(null=True)
    type = indexes.CharField()
    icon_name = indexes.CharField()

    # extra fields
    username = indexes.CharField(model_attr='username', stored=False)
    name = indexes.CharField(model_attr='get_full_name')
    email = indexes.CharField(model_attr='email', stored=False)
    institution = indexes.CharField(model_attr='institution', null=True)
    role = indexes.CharField(model_attr='role', null=True)
    google_talk = indexes.CharField(model_attr='google_talk', null=True,
                                    stored=False)
    webpage = indexes.CharField(model_attr='webpage', null=True, stored=False)
    message_count = indexes.IntegerField(stored=False)
    changeset_count = indexes.IntegerField(stored=False)
    ticket_count = indexes.IntegerField(stored=False)
    wiki_count = indexes.IntegerField(stored=False)
    contribution_count = indexes.IntegerField(stored=False)

    def get_model(self):
        return User

    @property
    def badge_counters(self):
        if not hasattr(self, '_badge_counters'):
            self._badge_counters = get_users_counters()
        return self._badge_counters

    def prepare(self, obj):
        prepared_data = super(UserIndex, self).prepare(obj)

        prepared_data['contribution_count'] = sum((
            self.prepared_data['message_count'],
            self.prepared_data['changeset_count'],
            self.prepared_data['ticket_count'],
            self.prepared_data['wiki_count']
        ))

        return prepared_data

    def prepare_description(self, obj):
        return u'{}\n{}\n{}\n{}'.format(
            obj.institution, obj.role, obj.username, obj.get_full_name()
        )

    def prepare_icon_name(self, obj):
        return u'user'

    def prepare_type(self, obj):
        return u'user'

    def prepare_message_count(self, obj):
        return self.badge_counters[obj.username]['messages']

    def prepare_changeset_count(self, obj):
        return self.badge_counters[obj.username]['revisions']

    def prepare_ticket_count(self, obj):
        return self.badge_counters[obj.username]['tickets']

    def prepare_wiki_count(self, obj):
        return self.badge_counters[obj.username]['wikis']

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_active=True)
