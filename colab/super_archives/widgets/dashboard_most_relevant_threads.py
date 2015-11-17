from colab.widgets.widget_manager import Widget
from django.template.loader import render_to_string


class DashboardMostRelevantThreadsWidget(Widget):
    name = 'most relevant threads'

    def get_body(self):
        return self.content

    def generate_content(self, **kwargs):
        template = 'widgets/dashboard_most_relevant_threads.html'
        self.content = render_to_string(template, kwargs.get('context'))
