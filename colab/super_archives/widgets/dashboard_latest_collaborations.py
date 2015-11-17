from colab.widgets.widget_manager import Widget
from django.template.loader import render_to_string


class DashboardLatestCollaborationsWidget(Widget):
    name = 'Latest Collaborations'

    def get_body(self):
        return self.content

    def generate_content(self, **kwargs):
        template = 'widgets/dashboard_latest_collaborations.html'
        self.content = render_to_string(template, kwargs.get('context'))
