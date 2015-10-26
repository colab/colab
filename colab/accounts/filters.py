from django.utils.translation import ugettext as _


def get_filters(request):
    return {
        'user': {
            'name': _(u'User'),
            'icon': 'user',
            'fields': (
                (
                    'username',
                    _(u'Username'),
                    request.get('username'),
                ),
                ('name', _(u'Name'), request.get('name')),
                (
                    'institution',
                    _(u'Institution'),
                    request.get('institution'),
                ),
                ('role', _(u'Role'), request.get('role'))
            ),
        },
    }
