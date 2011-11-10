
from super_archives.models import Thread, Vote, Message


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


def get_first_message_in_thread(thread_token):
    return get_messages_by_date().filter(thread__subject_token=thread_token)[0]
    

def get_latest_threads():
    return Thread.objects.order_by('-latest_message__received_time')


def get_voted_threads():
    """Query for the most voted threads sorting by the sum of votes 
    and latest messages received.
    
    NOTE: This implementation has serious performance issues on
    MySQL databases but it performes quite well on PostgreSQL.
    
    """
    
    sql = """
        SELECT 
            count(sav.id)
        FROM
            super_archives_message AS sam 
            JOIN super_archives_vote AS sav
                ON sav.message_id = sam.id
        WHERE
            super_archives_thread.id = sam.thread_id
    """

    threads = Thread.objects.extra(
        select={
            'vote_count': sql
        }
    )
    return threads.order_by('-vote_count', '-latest_message__received_time')
    
