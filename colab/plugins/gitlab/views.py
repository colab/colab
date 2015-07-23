
from ..utils.views import ColabProxyView
import os, sys


class GitlabProxyView(ColabProxyView):
    app_label = 'gitlab'
    diazo_theme_template = 'proxy/gitlab.html'


class GitlabProfileProxyView(ColabProxyView):
    app_label = 'gitlab'
    diazo_theme_template = 'proxy/gitlab_profile.html'

    @property
    def diazo_rules(self):
        child_class_file = sys.modules[self.__module__].__file__
        app_path = os.path.abspath(os.path.dirname(child_class_file))
        diazo_path = os.path.join(app_path, 'profile/diazo.xml')

        self.log.debug("diazo_rules: %s", diazo_path)
        return diazo_path
