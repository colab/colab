
from django.conf import settings

from ..utils.views import ColabProxyView


class JenkinsProxyView(ColabProxyView):
    upstream = settings.PROXIED_APPS['jenkins']['upstream']
