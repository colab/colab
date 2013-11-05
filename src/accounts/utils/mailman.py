
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
    print lists

    for maillist in current_lists:
        if maillist not in lists:
            unsubscribe(maillist, address)

    for maillist in lists:
        if maillist not in current_lists:
            subscribe(maillist, address)


def address_lists(address):
    url = get_url()
    try:
        lists = requests.get(url, timeout=TIMEOUT, params={'address': address})
    except requests.exceptions.RequestException:
        return []

    return lists.json()


def all_lists():
    return address_lists('')


def user_lists(user):
    list_set = set()

    for email in user.emails.values_list('address', flat=True):
        list_set.update(address_lists(email))

    return tuple(list_set)
