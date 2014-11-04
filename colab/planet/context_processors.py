
from django.conf import settings


def feedzilla(request):
    return {'feedzilla': getattr(settings, 'FEEDZILLA_ENABLED', False)}
