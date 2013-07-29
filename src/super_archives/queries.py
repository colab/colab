
from django.core.exceptions import ObjectDoesNotExist
from .models import Thread, Vote, Message, PageHit


def get_messages_by_date():
    return Message.objects.order_by('received_time')


def get_messages_by_voted():
    """Query for the most voted messages sorting by the sum of
    voted and after by date."""
    
    sql = """
        SELECT 
            count(sav.id)
        FROM
            super_archives_vote AS sav
        WHERE
            super_archives_message.id = sav.message_id
    """
    messages = Message.objects.extra(
        select={
            'vote_count': sql,
        }
    )
    return messages.order_by('-vote_count', 'received_time')


def get_first_message_in_thread(mailinglist, thread_token):
    query = get_messages_by_date()
    query = query.filter(thread__mailinglist__name=mailinglist)
    try:
        query = query.filter(thread__subject_token=thread_token)[0]
    except IndexError:
        raise ObjectDoesNotExist
    return query


def get_latest_threads():
    return Thread.objects.order_by('-latest_message__received_time')


def get_hottest_threads():
    return Thread.objects.order_by('-score', '-latest_message__received_time')


def get_page_hits(path_info):
    pagehit = PageHit.objects.filter(url_path=path_info)
    
    if pagehit:
        return pagehit[0].hit_count
    return 0

