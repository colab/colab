
from django.shortcuts import redirect

VIEW_NAMES_ALLOWED = ('signup', 'Logout')


class UserRegisterMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.is_ajax():
            return

        if not request.user.is_authenticated():
            return

        if not request.user.needs_update:
            return

        if view_func.__name__ not in VIEW_NAMES_ALLOWED:
            return redirect('signup')
