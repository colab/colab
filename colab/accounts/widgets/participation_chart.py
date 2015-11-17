from colab.widgets.widget_manager import Widget
from django.template.loader import render_to_string


class ParticipationChart(Widget):
    name = "participation_chart"

    def generate_content(self, **kwargs):
        self.content = render_to_string('widgets/participation_chart.html')
