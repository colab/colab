from django.conf import settings


def social_network_enabled(request):
    return {'SOCIAL_NETWORK_ENABLED': getattr(settings,
                                              'SOCIAL_NETWORK_ENABLED',
                                              False)}
