from django.db import models

from haystack.query import SearchQuerySet


class NotSpamManager(models.Manager):
    """Only return objects which are not marked as spam."""

    def get_queryset(self):
        return super(NotSpamManager, self).get_queryset().exclude(spam=True)


class HighestScore(NotSpamManager):
    def get_queryset(self):
        queryset = super(HighestScore, self).get_queryset()
        return queryset.order_by('-score', '-latest_message__received_time')

    def from_haystack(self):
        return SearchQuerySet().filter(type='thread')


class MostVotedManager(NotSpamManager):
    def get_queryset(self):
        """Query for the most voted messages sorting by the sum of
        voted and after by date."""

        queryset = super(MostVotedManager, self).get_queryset()

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
