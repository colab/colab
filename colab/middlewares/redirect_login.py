from django.utils import timezone
from datetime import timedelta
from django.core.urlresolvers import reverse

class RedirectLoginMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            return

        if request.is_ajax():
            return

        if 'text/html' in request.META['HTTP_ACCEPT']:
            if request.path != reverse('login'):
                cookie_expire = timezone.now() + timedelta(minutes=1)
                print cookie_expire
                request.COOKIES.set('_previous_path', value=request.path,
                                    expires=cookie_expire, max_age=10)
