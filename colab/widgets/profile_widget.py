from colab.widgets.widget_manager import Widget
from django.conf import settings


class ProfileWidget(Widget):
    app_name = None
    colab_form = None
    request = None
    _prefix = None
    bootstrap_conflict = False
    jquery_conflict = False

    @property
    def prefix(self):
        if self._prefix is None:
            urls = settings.COLAB_APPS[self.app_name].get('urls')
            self._prefix = urls.get('prefix').replace('^', '/')
        return self._prefix

    def default_url(self, request):
        raise NotImplementedError("Please Implement this method")

    def fix_url(self, url):
        cut = 0
        if self.prefix in url:
            cut = url.find(self.prefix) + len(self.prefix)
        return url[cut:]

    def is_colab_form(self, request):
        if self.colab_form is None:
            self.colab_form = request.POST.get('colab_form', False)
        return self.colab_form

    def must_respond(self, request):
        if self.is_colab_form(request):
            return False
        return self.prefix in request.GET.get('path', '') or \
            self.prefix in request.POST.get('path', '')

    def change_request_method(self, request):
        request.method = 'GET'

        if self.must_respond(request) and len(request.POST) > 0:
            if not request.POST.get('_method', None):
                request.method = "POST"
            else:
                request.method = request.POST.get("_method").upper()

    def requested_url(self, request):
        url = request.POST.get('path', request.GET.get('path', ''))

        if not url or not self.must_respond(request):
            url = self.default_url(request)

        return self.fix_url(url)

    def dispatch(self, request, url):
        raise NotImplementedError("Please Implement this method")

    def generate_content(self, **kwargs):
        request = kwargs.get('context', {}).get('request', None)
        self.change_request_method(request)
        response = self.dispatch(request, self.requested_url(request))

        if hasattr(response, 'content'):
            self.content = response.content
        else:
            self.content = "".join(response.streaming_content)
