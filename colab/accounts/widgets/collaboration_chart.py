from colab.widgets.widget_manager import Widget
from django.template.loader import render_to_string


class CollaborationChart(Widget):
    name = "collaboration_chart"

    def generate_content(self, **kwargs):
        self.content = render_to_string('widgets/collaboration_chart.html')
