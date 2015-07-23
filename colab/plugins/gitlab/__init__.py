

default_app_config = 'colab.plugins.gitlab.apps.ProxyGitlabAppConfig'

from colab.plugins.utils.widget_manager import WidgetManager
from colab.plugins.gitlab.widgets import GitlabProfileWidget

WidgetManager.register_widget('profile', GitlabProfileWidget())
