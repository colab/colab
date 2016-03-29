from django.utils import timezone
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.conf import settings


class RedirectLoginMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            return

        if request.is_ajax():
            return

        if request.path == reverse('login'):
            return

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            if request.path not in settings.COLAB_APPS_LOGIN_URLS:
                cookie_expire = timezone.now() + timedelta(minutes=1)
                request.COOKIES.set('_previous_path', value=request.path,
                                    expires=cookie_expire, max_age=10)
