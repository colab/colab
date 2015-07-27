
import urlparse
import requests
import logging

from django.conf import settings
from django.contrib import messages

TIMEOUT = 1

LOGGER = logging.getLogger('colab.mailman')

S = 'success'
I = 'info'
E = 'error'

MAILMAN_MSGS = {
    0: (S, '%s: Success!'),
    1: (S, '%s: An email confirmation was sent to you, please check your inbox.'),
    2: (I, '%s: Your subscription was sent successfully! Please wait for the list\'s admin approval.'),
    3: (I, '%s: You are already a member of this list.'),
    4: (E, '%s: You are banned from this list!'),
    5: (E, '%s: You appear to have an invalid email address.'),
    6: (E, '%s: Your email address is considered to be hostile.'),
    7: (E, '%s: You are not a member of this list.'),
    8: (E, 'Missing information: `email_from`, `subject` and `body` are mandatory.'),
}


def get_url(listname=None):
    if listname:
        return urlparse.urljoin(settings.MAILMAN_API_URL, listname)

    return settings.MAILMAN_API_URL


def subscribe(listname, address):
    url = get_url(listname)
    try:
        result = requests.put(url, timeout=TIMEOUT, data={'address': address})
        msg_type, message = MAILMAN_MSGS[result.json()]
        return msg_type, message % listname
    except:
        LOGGER.exception('Unable to subscribe user')
        return E, 'Error: Unable to subscribe user'


def unsubscribe(listname, address):
    url = get_url(listname)
    try:
        result = requests.delete(url, timeout=TIMEOUT, data={'address': address})
        return True, '%s: %s' % (listname, result.json())
    except:
        LOGGER.exception('Unable to unsubscribe user')
        return False, 'Error: Unable to unsubscribe user'


def update_subscription(address, lists):
    current_lists = mailing_lists(address=address)
    info_messages = []

    for maillist in current_lists:
        if maillist not in lists:
            info_messages.append(unsubscribe(maillist, address))

    for maillist in lists:
        if maillist not in current_lists:
            info_messages.append(subscribe(maillist, address))

    return info_messages


def mailing_lists(**kwargs):
    url = get_url()

    try:
        lists = requests.get(url, timeout=TIMEOUT, params=kwargs)
    except:
        LOGGER.exception('Unable to list mailing lists')
        return []

    return lists.json()


def is_private_list(name):
    try:
        return dict(all_lists(private=True))[name]
    except KeyError:
        return []


def all_lists(**kwargs):
    return mailing_lists(**kwargs)


def user_lists(user):
    list_set = set()

    for email in user.emails.values_list('address', flat=True):
        list_set.update(mailing_lists(address=email))

    return tuple(list_set)


def get_list_description(listname, lists=None):
    if not lists:
        lists = dict(all_lists(description=True))
    elif not isinstance(lists, dict):
        lists = dict(lists)

    return lists.get(listname)


def list_users(listname):
    url = get_url(listname)

    params = {}

    try:
        users = requests.get(url, timeout=TIMEOUT, params=params)
    except requests.exceptions.RequestException:
        return []

    return users.json()


def get_user_mailinglists(user):
    lists_for_user = []
    emails = ''

    if user:
        emails = user.emails.values_list('address', flat=True)

    for email in emails:
        lists_for_user.extend(mailing_lists(address=email))

    return lists_for_user
