# -*- coding: utf-8 -*-

from django.db.models import Count

from proxy.models import Revision, Ticket, Wiki
from super_archives.models import Message


def get_counters_to_badge(user):
    count_revisions = Revision.objects.filter(author=user.username).count()
    count_tickets = Ticket.objects.filter(author=user.username).count()
    count_wikis = Wiki.objects.filter(author=user.username).count()

    return dict(
        messages=user.emails.aggregate(Count('message'))['message__count'],
        revisions=count_revisions,
        tickets=count_tickets,
        wikis=count_wikis,
        contributions=count_revisions + count_tickets + count_wikis,
    )

# using haystack
# sqs = SearchQuerySet()
# sqs.filter(type='changeset', author=user.get_full_name()).count()
# sqs.filter(type='wiki', author=user.get_full_name()).count()
# sqs.filter(type='ticket', author=user.get_full_name()).count()
# Should it use the author_and_username attr too?
