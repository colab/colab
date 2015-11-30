from django.conf import settings
from django.utils.translation import ugettext_lazy as _


def robots(request):
    return {'ROBOTS_NOINDEX': getattr(settings, 'ROBOTS_NOINDEX', False)}


def google_analytics(request):
    key = 'GOOGLE_ANALYTICS_TRACKING_ID'
    return {key: getattr(settings, key, False)}


def ribbon(request):
    enabled = getattr(settings, 'RIBBON_ENABLED', True)
    if not enabled:
        return {'ribbon': False}

    url = 'http://github.com/colab/colab'
    text = _('Fork me!')

    return {
        'ribbon': {
            'text': getattr(settings, 'RIBBON_TEXT', text),
            'url': getattr(settings, 'RIBBON_URL', url),
        }
    }
