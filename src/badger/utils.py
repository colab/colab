# -*- coding: utf-8 -*-

from django.db.models import Count

from proxy.models import (Revision, Ticket, Wiki,
                          WikiCollabCount, TicketCollabCount)
from accounts.models import User


def get_wiki_counters():
    return {author: count for author, count in
            WikiCollabCount.objects.values_list()}


def get_revision_counters():
    return {
        author: count for author, count in Revision.objects.values_list(
            'author'
        ).annotate(count=Count('author'))
    }


def get_ticket_counters():
    return {author: count for author, count in
            TicketCollabCount.objects.values_list()}


def get_users_counters():
    wiki_counters = get_wiki_counters()
    revision_counters = get_revision_counters()
    ticket_counters = get_ticket_counters()

    users_counters = {}
    for user in User.objects.annotate(message_count=Count('emails__message')):
        users_counters[user.username] = {
            'messages': user.message_count,
            'wikis': wiki_counters.get(user.username, 0),
            'revisions': revision_counters.get(user.username, 0),
            'tickets': ticket_counters.get(user.username, 0),
        }
    return users_counters
