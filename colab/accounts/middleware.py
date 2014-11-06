from json import dumps as json_dumps

from colab.accounts.models import User
from colab.proxy.utils.views import ColabProxyView


class RemoteUserMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            return

        if not hasattr(view_func, 'im_class'):
            return

        if not issubclass(view_func.im_class, ColabProxyView):
            return

        user = User.objects.get(
            username=request.user.get_username()
            )

        remote_user_data = {}

        remote_user_data['email'] = user.email
        remote_user_data['name'] = user.username

        request.META['REMOTE_USER_DATA'] = json_dumps(
            remote_user_data,
            sort_keys=True,
            )

        return None
