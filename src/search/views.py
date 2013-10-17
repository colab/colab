# -*- coding:utf-8 -*-

from django.conf import settings
from haystack.views import SearchView


class ColabSearchView(SearchView):
    def extra_context(self, *args, **kwargs):
        # Retornar todos os campos de cada tipo a serem filtrados
        # retornar os nomes dos campos
        # retornar os ícones dos tipos

        # a critical point on the system
        types = {
            'wiki': {
                'icon': 'file',
                'fields': [
                    'title', 'description', 'author', 'collaborators',
                    'created', 'modified',
                ],
            },
            'discussion': {
                'icon': 'thread',
                'fields': [
                    'title', 'description', 'created', 'modified', 'author',
                    'tag',
                ],
            },
            'ticket': {
                'icon': 'ticket',
                'fields': [
                    'title', 'description', 'milestone', 'priority',
                    'component', 'version', 'severity', 'reporter', 'author',
                    'status', 'keywords', 'collaborators', 'created',
                    'modified',
                ],
            },
            'changeset': {
                'icon': 'changeset',
                'fields': [
                    'title', 'author', 'description', 'repository_name',
                    'created', 'modified',
                ],
            },
            'user': {
                'icon': 'user',
                'fields': [
                    'title', 'description', 'username', 'name',
                    'email', 'institution', 'role', 'google_talk', 'webpage',
                ],
            },
        }
        types = self.form.cleaned_data['type']
        return dict(
            types=types.split(),
            types_str=types,
            order_data=settings.ORDERING_DATA
        )
