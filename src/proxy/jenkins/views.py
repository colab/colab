
from django.conf import settings

from ..utils import ColabProxyView


class JenkinsProxyView(ColabProxyView):
    upstream = settings.COLAB_CI_URL
