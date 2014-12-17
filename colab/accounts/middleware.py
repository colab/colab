from django.core.urlresolvers import resolve
from django.shortcuts import redirect


class UserRegisterMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            return

        if not request.user.needs_update:
            return

        current_url = resolve(request.path_info).url_name

        if current_url not in ['signup']:
            return redirect('signup')

        return None
