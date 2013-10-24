# -*- coding:utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext as _

from haystack.views import SearchView


class ColabSearchView(SearchView):
    def extra_context(self, *args, **kwargs):

        use_language, date_format = settings.DJANGO_DATE_FORMAT_TO_JS.get(
            self.request.LANGUAGE_CODE, (None, None)
        )

        types = {
            'wiki': {
                'name': _(u'Wiki'),
                'fields': (
                    ('author', _(u'Author'), self.request.GET.get('author')),
                    (
                        'collaborators',
                        _(u'Collaborators'),
                        self.request.GET.get('collaborators'),
                    ),
                ),
            },
            'thread': {
                'name': _(u'Discussion'),
                'fields': (
                    ('author', _(u'Author'), self.request.GET.get('author')),
                    (
                        'list',
                        _(u'Mailinglist'),
                        self.request.GET.getlist('list')
                    ),
                ),
            },
            'ticket': {
                'name': _(u'Ticket'),
                'fields': (
                    (
                        'milestone',
                        _(u'Milestone'),
                        self.request.GET.get('milestone')
                    ),
                    (
                        'priority',
                        _(u'Priority'),
                        self.request.GET.get('priority')
                    ),
                    (
                        'component',
                        _(u'Component'),
                        self.request.GET.get('component')
                    ),
                    (
                        'severity',
                        _(u'Severity'),
                        self.request.GET.get('severity')
                    ),
                    (
                        'reporter',
                        _(u'Reporter'),
                        self.request.GET.get('reporter')
                    ),
                    ('author', _(u'Author'), self.request.GET.get('author')),
                    ('tag', _(u'Status'), self.request.GET.get('tag')),
                    (
                        'keywords',
                        _(u'Keywords'),
                        self.request.GET.get('keywords'),
                    ),
                    (
                        'collaborators',
                        _(u'Collaborators'),
                        self.request.GET.get('collaborators')
                    ),
                ),
            },
            'changeset': {
                'name': _(u'Changeset'),
                'fields': (
                    ('author', _(u'Author'), self.request.GET.get('author')),
                    (
                        'repository_name',
                        _(u'Repository'),
                        self.request.GET.get('repository_name'),
                    ),
                )
            },
            'user': {
                'name': _(u'User'),
                'fields': (
                    (
                        'username',
                        _(u'Username'),
                        self.request.GET.get('username'),
                    ),
                    ('name', _(u'Name'), self.request.GET.get('name')),
                    (
                        'institution',
                        _(u'Institution'),
                        self.request.GET.get('institution'),
                    ),
                    ('role', _(u'Role'), self.request.GET.get('role'))
                ),
            },
        }

        try:
            type_chosen = self.form.cleaned_data.get('type')
        except AttributeError:
            type_chosen = ''

        return dict(
            filters=types.get(type_chosen),
            type_chosen=type_chosen,
            order_data=settings.ORDERING_DATA,
            date_format=date_format,
            use_language=use_language,
        )
