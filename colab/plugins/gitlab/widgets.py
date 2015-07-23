from colab.plugins.gitlab.views import GitlabProxyView, GitlabProfileProxyView
from colab.plugins.utils.widget_manager import Widget
from django.utils.safestring import mark_safe


class GitlabProfileWidget(GitlabProxyView, Widget):
    identifier = 'code'
    name = 'Gitlab Profile'
    default_url = '/gitlab/profile/account'

    def generate_content(self, request):
        requested_url = request.GET.get('code', self.default_url)
        g = GitlabProfileProxyView()
        r = g.dispatch(request, requested_url)
        if r.status_code == 302:
            location = r.get('Location')
            requested_url = location[location.find('/{}/'.format(self.app_label)):]
            request.method = 'GET'
            r = g.dispatch(request, requested_url)

        return "<div>" + r.content + "</div>"