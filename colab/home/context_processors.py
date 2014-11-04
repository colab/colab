from django.conf import settings
from django.utils.translation import ugettext_lazy as _


def robots(request):
    return {'ROBOTS_NOINDEX': getattr(settings, 'ROBOTS_NOINDEX', False)}


def ribbon(request):
    enabled = getattr(settings, 'RIBBON_ENABLED', True)
    if not enabled:
        return {'ribbon': False}

    url = 'http://beta.softwarepublico.gov.br/gitlab/softwarepublico/colab'
    text = _('Fork me!')

    return {
         'ribbon': {
            'text': getattr(settings, 'RIBBON_TEXT', text),
            'url': getattr(settings, 'RIBBON_URL', url),
        }
    }
