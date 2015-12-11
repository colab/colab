
import json

from django.conf import settings

from revproxy.views import DiazoProxyView

from .conf import get_plugin_config


class ColabProxyView(DiazoProxyView):
    add_remote_user = settings.REVPROXY_ADD_REMOTE_USER
    diazo_theme_template = 'base.html'
    html5 = True

    @property
    def upstream(self):
        config = get_plugin_config(self.app_label)
        return config.get('upstream')

    @property
    def app_label(self):
        raise NotImplementedError('app_label attribute must be set')

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        if request.user.is_authenticated():

            remote_user_data = {}

            remote_user_data['email'] = request.user.email
            remote_user_data['name'] = request.user.get_full_name()

            request.META['HTTP_REMOTE_USER_DATA'] = json.dumps(
                remote_user_data,
                sort_keys=True,
                )

        return super(ColabProxyView, self).dispatch(request, *args, **kwargs)
