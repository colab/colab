from colab.widgets.widget_manager import Widget
from django.template.loader import render_to_string


class DashboardLatestThreadsWidget(Widget):
    name = 'latest threads'

    def get_body(self):
        return self.content

    def generate_content(self, **kwargs):
        template = 'widgets/dashboard_latest_threads.html'
        self.content = render_to_string(template, kwargs.get('context'))
