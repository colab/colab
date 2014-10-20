from django.conf import settings

def robots(request):
    return {'ROBOTS_NOINDEX': getattr(settings, 'ROBOTS_NOINDEX', False)}
