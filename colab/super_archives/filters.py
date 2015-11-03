from django.utils.translation import ugettext as _
from colab.super_archives.models import MailingList


def get_filters(request):
    return {
        'thread': {
            'name': _(u'Discussion'),
            'icon': 'envelope',
            'fields': (
                ('author', _(u'Author'), request.get('author')),
                (
                    'list',
                    _(u'Mailinglist'),
                    request.get('list'),
                    'list',
                    [(v, v) for v in MailingList.objects.values_list(
                        'name', flat=True)]
                ),
            ),
        },
    }
