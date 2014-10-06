
from django.conf import settings

from ..utils.views import ColabProxyView


class JenkinsProxyView(ColabProxyView):
    app_label = 'jenkins'
