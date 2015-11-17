from colab.widgets.widget_manager import Widget
from django.template.loader import render_to_string


class DashboardCollaborationGraphWidget(Widget):
    name = 'Collaboration Graph'

    def generate_content(self, **kwargs):
        template = 'widgets/dashboard_collaboration_graph.html'
        self.content = render_to_string(template, kwargs.get('context'))
