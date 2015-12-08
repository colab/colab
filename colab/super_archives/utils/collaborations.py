
from django.db.models import Q

from colab.accounts.utils import mailman
from colab.super_archives.models import Thread, Message


def count_threads():
    return Thread.objects.count()


def get_visible_threads_queryset(logged_user):
    queryset = Thread.objects
    listnames_for_user = []
    if logged_user:
        lists_for_user = mailman.get_user_mailinglists(logged_user)
        listnames_for_user = mailman.extract_listname_from_list(lists_for_user)

    user_lists = Q(mailinglist__name__in=listnames_for_user)
    public_lists = Q(mailinglist__is_private=False)
    queryset = Thread.objects.filter(user_lists | public_lists)

    return queryset


def get_visible_threads(logged_user, filter_by_user=None):
    thread_qs = get_visible_threads_queryset(logged_user)

    if filter_by_user:
        message_qs = Message.objects.filter(thread__in=thread_qs)
        messages = message_qs.filter(
            from_address__user__pk=filter_by_user.pk)
    else:
        latest_threads = thread_qs.all()
        messages = [t.latest_message for t in latest_threads]

    return messages
