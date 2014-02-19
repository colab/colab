
import urlparse
import requests

from django.conf import settings

TIMEOUT = 1


def get_url(listname=None):
    if listname:
        return urlparse.urljoin(settings.MAILMAN_API_URL, '/' + listname)

    return settings.MAILMAN_API_URL


def subscribe(listname, address):
    url = get_url(listname)
    try:
        requests.put(url, timeout=TIMEOUT, data={'address': address})
    except requests.exceptions.RequestException:
        return False
    return True


def unsubscribe(listname, address):
    url = get_url(listname)
    try:
        requests.delete(url, timeout=TIMEOUT, data={'address': address})
    except requests.exceptions.RequestException:
        return False
    return True


def update_subscription(address, lists):
    current_lists = address_lists(address)

    for maillist in current_lists:
        if maillist not in lists:
            unsubscribe(maillist, address)

    for maillist in lists:
        if maillist not in current_lists:
            subscribe(maillist, address)


def address_lists(address, description=''):
    url = get_url()

    params = {'address': address,
              'description': description}

    try:
        lists = requests.get(url, timeout=TIMEOUT, params=params)
    except requests.exceptions.RequestException:
        return []

    return lists.json()


def all_lists(*args, **kwargs):
    return address_lists('', *args, **kwargs)


def user_lists(user):
    list_set = set()

    for email in user.emails.values_list('address', flat=True):
        list_set.update(address_lists(email))

    return tuple(list_set)


def get_list_description(listname, lists=None):
    if not lists:
        lists = dict(all_lists(description=True))
    elif not isinstance(lists, dict):
        lists = dict(lists)

    return lists.get(listname)
