from django.db import models

from haystack.query import SearchQuerySet
import django

class NotSpamManager(models.Manager):
    """Only return objects which are not marked as spam."""

    def get_queryset(self):
        if django.VERSION < (1, 7):
            return super(NotSpamManager, self).get_queryset().exclude(spam=True)
        else:
            return super(NotSpamManager, self).get_query_set().exclude(spam=True)

    if django.VERSION < (1, 7):
        # in 1.7+, get_query_set gets defined by the base ChangeList and complains if it's called.
        # otherwise, we have to define it ourselves.
        get_query_set = get_queryset


class HighestScore(NotSpamManager):
    def get_queryset(self):
        if django.VERSION < (1, 7):
            queryset = super(HighestScore, self).get_queryset()
        else:
            queryset = super(HighestScore, self).get_query_set()
        return queryset.order_by('-score', '-latest_message__received_time')

    def from_haystack(self):
        return SearchQuerySet().filter(type='thread')


class MostVotedManager(NotSpamManager):
    def get_queryset(self):
        """Query for the most voted messages sorting by the sum of
        voted and after by date."""

        if django.VERSION < (1, 7):
            queryset = super(MostVotedManager, self).get_queryset()
        else:
            queryset = super(MostVotedManager, self).get_query_set()

        sql = """
            SELECT
                count(sav.id)
            FROM
                super_archives_vote AS sav
            WHERE
                super_archives_message.id = sav.message_id
        """

        messages = queryset.extra(
            select={
                'vote_count': sql,
            }
        )
        return messages.order_by('-vote_count', 'received_time')
