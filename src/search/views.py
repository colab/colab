# -*- coding:utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext as _

from haystack.views import SearchView


class ColabSearchView(SearchView):
    def extra_context(self, *args, **kwargs):
        types = {
            'wiki': {
                'icon': 'file',
                'name': _(u'Wiki'),
                'fields': {'author': _(u'Author')},
            },
            'thread': {
                'icon': 'thread',
                'name': _(u'Discussion'),
                'fields': {'author': _(u'Author'), 'list': _(u'Mailinglist')},
            },
            'ticket': {
                'icon': 'ticket',
                'name': _(u'Ticket'),
                'fields': {
                    'milestone': _(u'Milestone'), 'priority': _(u'Priority'),
                    'component': _(u'Component'), 'severity': _(u'Severity'),
                    'reporter': _(u'Reporter'), 'author': _(u'Author'),
                    'tag': _(u'Status'), 'keywords': _(u'Keywords'),
                    'collaborators': _(u'Collaborators'),
                },
            },
            'changeset': {
                'icon': 'changeset',
                'name': _(u'Changeset'),
                'fields': {'author': _(u'Author'), 'repository_name': _(u'Repository')},
            },
            'user': {
                'icon': 'user',
                'name': _(u'User'),
                'fields': {'username': _(u'Username'), 'name': _(u'Name'), 'institution': _(u'Institution'), 'role': _(u'Role')},
            },
        }

        try:
            type_chosen = self.form.cleaned_data.get('type')
        except AttributeError:
            type_chosen = ''

        return dict(
            filters=types.get(type_chosen),
            type_chosen=type_chosen,
            order_data=settings.ORDERING_DATA
        )
