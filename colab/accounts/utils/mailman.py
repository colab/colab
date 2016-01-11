import logging
import requests
import urlparse

from uuid import uuid4

from django.conf import settings
from django.core import mail
from django.template import Context, loader
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

TIMEOUT = 1

LOGGER = logging.getLogger('colab.mailman')

S = 'success'
I = 'info'
E = 'error'

MAILMAN_MSGS = {
    0: (S, '%s: Success!'),
    1: (S, '%s: An email confirmation was sent to you, please check your \
inbox.'),
    2: (I, '%s: Your subscription was sent successfully! Please wait for the \
list\'s admin approval.'),
    3: (I, '%s: You are already a member of this list.'),
    4: (E, '%s: You are banned from this list!'),
    5: (E, '%s: You appear to have an invalid email address.'),
    6: (E, '%s: Your email address is considered to be hostile.'),
    7: (E, '%s: You are not a member of this list.'),
    8: (E, 'Missing information: `email_from`, `subject` and `body` are \
mandatory.'),
    9: (E, 'Bad list name'),
    10: (E, 'AssertionError'),
    11: (E, 'Invalid password'),
    12: (E, 'Mailman unknown list error'),
    13: (E, 'List already exists'),
    14: (E, 'Invalid params'),
}


def send_create_list_email(**kargs):
    """ Send the notification mail
    kargs' params:
        user = User object
        password = list's password
        listname = list's name
    """
    to = kargs.get('user', None)
    if not to:
        return

    to = [to.email]
    from_email = settings.COLAB_FROM_ADDRESS
    subject = _('Created list {}.'.format(kargs.get('listname', '')))
    msg_tmpl = loader.get_template('emails/create_list_confirmation.txt')
    message = msg_tmpl.render(Context(kargs))
    return mail.send_mail(subject, message, from_email, to)


def create_list(listname, admin):
    url = get_url('lists/', listname=listname)
    password = uuid4().hex
    try:
        # By default, the password is the name of the list
        admin_user = get_user_model().objects.get(username=admin.username)
        result = requests.post(url, timeout=TIMEOUT, data={
                               'admin': admin_user.email,
                               'password': password})
        msg_type, message = MAILMAN_MSGS[result.json()]
        send_create_list_email(
            user=admin_user,
            password=password,
            listname=listname
        )
        return msg_type, message % listname
    except:
        LOGGER.exception('Unable to create list')
        return E, 'Error: Unable to create list'


def get_url(path, listname=None):
    url = urlparse.urljoin(settings.MAILMAN_API_URL, path)
    if listname:
        return urlparse.urljoin(url, listname)
    return url


def subscribe(listname, address):
    url = get_url('subscribe/', listname=listname)
    try:
        result = requests.put(url, timeout=TIMEOUT, data={'address': address})
        msg_type, message = MAILMAN_MSGS[result.json()]
        return msg_type, message % listname
    except:
        LOGGER.exception('Unable to subscribe user')
        return E, 'Error: Unable to subscribe user'


def unsubscribe(listname, address):
    url = get_url('subscribe/', listname)
    try:
        result = requests.delete(url, timeout=TIMEOUT, data={'address':
                                                             address})
        msg_type, message = MAILMAN_MSGS[result.json()]
        return msg_type, message % listname
    except:
        LOGGER.exception('Unable to unsubscribe user')
        return E, 'Error: Unable to subscribe user'


def update_subscription(address, lists):
    current_lists = mailing_lists(address=address, names_only=True)
    info_messages = []

    for maillist in current_lists:
        if maillist not in lists:
            info_messages.append(unsubscribe(maillist, address))

    for maillist in lists:
        if maillist not in current_lists:
            info_messages.append(subscribe(maillist, address))

    return info_messages


def mailing_lists(**kwargs):
    url = get_url('lists/')

    try:
        lists = requests.get(url, timeout=TIMEOUT, params=kwargs).json()
        if not isinstance(lists, (list, tuple)):
            raise
    except:
        LOGGER.exception('Unable to list mailing lists')
        return []

    if kwargs.get('names_only'):
        names_only = []
        for l in lists:
            names_only.append(l['listname'])
        return names_only
    else:
        return lists


def is_private_list(name):
    try:
        privacy = {}
        privacy.update({mlist.get('listname'): mlist.get('archive_private')
                        for mlist in all_lists()})
        return privacy[name]
    except KeyError:
        return []


def all_lists(**kwargs):
    return mailing_lists(**kwargs)


def user_lists(user):
    list_set = set()

    for email in user.emails.values_list('address', flat=True):
        mlists = mailing_lists(address=email)
        list_set.update(mlist.get('listname') for mlist in mlists)

    return tuple(list_set)


def get_list_description(listname, lists=None):
    if not lists:
        lists = all_lists()

    desc = "".join(mlist.get('description') for mlist in lists
                   if isinstance(mlist, dict) and
                   mlist.get('listname') == listname)

    return desc


def list_users(listname):
    url = get_url('members/', listname)

    params = {}

    try:
        users = requests.get(url, timeout=TIMEOUT, params=params)
    except requests.exceptions.RequestException:
        return []

    result = users.json()
    if isinstance(result, int):
        LOGGER.error('Error number %s', result)
        return []

    return result


def get_user_mailinglists(user):
    lists_for_user = []
    emails = ''

    if user:
        emails = user.emails.values_list('address', flat=True)

    for email in emails:
        lists_for_user.extend(mailing_lists(address=email))

    return lists_for_user


def extract_listname_from_list(lists):
    try:
        return [mlist.get('listname') for mlist in lists]
    except ValueError:
        LOGGER.exception('listname not available')
        return []
