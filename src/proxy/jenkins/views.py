
from django.conf import settings

from ..utils.views import ColabProxyView


class JenkinsProxyView(ColabProxyView):
    upstream = settings.COLAB_CI_URL
