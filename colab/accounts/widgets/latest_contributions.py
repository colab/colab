from colab.widgets.widget_manager import Widget
from django.template.loader import render_to_string


class LatestContributionsWidget(Widget):
    name = 'latest contributionsp'

    def get_body(self):
        return self.content

    def generate_content(self, **kwargs):
        self.content = render_to_string('widgets/latest_contributions.html',
                                        kwargs.get('context'))
