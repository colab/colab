
from django.utils.translation import ugettext as _


def trans(key):
    translations = {
        'wiki': _('Wiki'),
        'thread': _('Emails'),
        'changeset': _('Code'),
        'ticket': _('Tickets'),
    }

    return translations.get(key, key)
