# -*- coding:utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext as _

from haystack.views import SearchView
from colab.plugins.utils import filters_importer

class ColabSearchView(SearchView):
    def extra_context(self, *args, **kwargs):

        use_language, date_format = settings.DJANGO_DATE_FORMAT_TO_JS.get(
            self.request.LANGUAGE_CODE, (None, None)
        )

        types = {
            'thread': {
                'name': _(u'Discussion'),
                'icon': 'envelope',
                'fields': (
                    ('author', _(u'Author'), self.request.GET.get('author')),
                    (
                        'list',
                        _(u'Mailinglist'),
                        self.request.GET.getlist('list')
                    ),
                ),
            },
        }

        types['user'] = {
            'name': _(u'User'),
            'icon': 'user',
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
        }

        try:
            type_chosen = self.form.cleaned_data.get('type')
        except AttributeError:
            type_chosen = ''

        mimetype_choices = ()
        size_choices = ()
        used_by_choices = ()

        mimetype_chosen = self.request.GET.get('mimetype')
        size_chosen = self.request.GET.get('size')
        used_by_chosen = self.request.GET.get('used_by')

        types.update(filters_importer.import_plugin_filters(self.request))

        filters_options = [(k, v['name'], v['icon']) \
                for (k,v) in types.iteritems()]
        return dict(
            filters=types.get(type_chosen),
            filters_options=filters_options,
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
