from django.conf import settings
from django.core.urlresolvers import reverse


def social_network_enabled(request):
    return {'SOCIAL_NETWORK_ENABLED': getattr(settings,
                                              'SOCIAL_NETWORK_ENABLED',
                                              False)}


def redirect_login(request):
    previous_path = request.COOKIES.get('_previous_path')
    if previous_path is None:
        return {'previous_path': reverse('home')}
    else:
        return {'previous_path': previous_path}
