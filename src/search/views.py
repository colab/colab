# -*- coding:utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext as _

from haystack.views import SearchView

from proxy.models import Attachment


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
            'attachment': {
                'name': _(u'Attachment'),
                'fields': (
                    (
                        'filename',
                        _(u'Filename'),
                        self.request.GET.get('filename')
                    ),
                    ('author', _(u'Author'), self.request.GET.get('author')),
                    (
                        'used_by',
                        _(u'Used by'), self.request.GET.get('used_by')),
                    (
                        'mimetype',
                        _(u'File type'),
                        self.request.GET.get('mimetype')
                    ),
                    ('size', _(u'Size'), self.request.GET.get('size')),
                )
            }
        }

        try:
            type_chosen = self.form.cleaned_data.get('type')
        except AttributeError:
            type_chosen = ''

        mimetype_choices = ()
        size_choices = ()
        used_by_choices = ()

        if type_chosen == 'attachment':
            mimetype_choices = [(type_, display) for type_, display, mimelist_ in settings.FILE_TYPE_GROUPINGS]
            size_choices = [
                ('<500KB', u'< 500 KB'),
                ('500KB__10MB', u'>= 500 KB <= 10 MB'),
                ('>10MB', u'> 10 MB'),
            ]
            used_by_choices = set([
                (v, v) for v in Attachment.objects.values_list(
                'used_by', flat=True)
            ])

        mimetype_chosen = self.request.GET.get('mimetype')
        size_chosen = self.request.GET.get('size')
        used_by_chosen = self.request.GET.get('used_by')

        return dict(
            filters=types.get(type_chosen),
            type_chosen=type_chosen,
            order_data=settings.ORDERING_DATA,
            date_format=date_format,
            use_language=use_language,
            mimetype_chosen=mimetype_chosen if mimetype_chosen else '',
            mimetype_choices=mimetype_choices,
            size_chosen=size_chosen if size_chosen else '',
            size_choices=size_choices,
            used_by_chosen=used_by_chosen if used_by_chosen else '',
            used_by_choices=used_by_choices,
        )
