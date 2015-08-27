from colab.plugins.gitlab.views import GitlabProxyView, GitlabProfileProxyView
from colab.plugins.utils.widget_manager import Widget
from django.utils.safestring import mark_safe


class GitlabProfileWidget(GitlabProxyView, Widget):
    identifier = 'code'
    name = 'Gitlab Profile'
    default_url = '/gitlab/profile/account'

    def get_body(self):
        start = self.content.find('<body')
        start = self.content.find('>', start)
        end = self.content.find('</body>')
        print "start = " + str(start) + ", end = " + str(end)
        print "content = " + self.content

        if -1 in [start, end]:
            return ''

        body = self.content[start + len('>'):end]
        return mark_safe(body)

    def generate_content(self, request):
        requested_url = request.GET.get('code', self.default_url)
        g = GitlabProfileProxyView()
        r = g.dispatch(request, requested_url)

        if r.status_code == 302:
            location = r.get('Location')
            requested_url = location[location.find('/{}/'.format(self.app_label)):]
            request.method = 'GET'
            r = g.dispatch(request, requested_url)

        self.content = r.content
