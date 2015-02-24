
import urlparse
import requests
import logging

from django.conf import settings

TIMEOUT = 1

LOGGER = logging.getLogger('colab.mailman')


def get_url(listname=None):
    if listname:
        return urlparse.urljoin(settings.MAILMAN_API_URL, '/' + listname)

    return settings.MAILMAN_API_URL


def subscribe(listname, address):
    url = get_url(listname)
    try:
        requests.put(url, timeout=TIMEOUT, data={'address': address})
    except:
        LOGGER.exception('Unable to subscribe user')
        return False
    return True


def unsubscribe(listname, address):
    url = get_url(listname)
    try:
        requests.delete(url, timeout=TIMEOUT, data={'address': address})
    except:
        LOGGER.exception('Unable to unsubscribe user')
        return False
    return True


def update_subscription(address, lists):
    current_lists = mailing_lists(address=address)

    for maillist in current_lists:
        if maillist not in lists:
            unsubscribe(maillist, address)

    for maillist in lists:
        if maillist not in current_lists:
            subscribe(maillist, address)


def address_lists(address):
    return mailing_lists(address=address)


def mailing_lists(**kwargs):
    url = get_url()

    try:
        lists = requests.get(url, timeout=TIMEOUT, params=kwargs)
    except:
        LOGGER.exception('Unable to list mailing lists')
        return []

    return lists.json()


def is_private_list(name):
    return dict(all_lists(private=True))[name]


def all_lists(*args, **kwargs):
    return mailing_lists(*args, **kwargs)


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
