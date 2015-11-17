from colab.widgets.widget_manager import Widget
from django.template.loader import render_to_string


class GroupWidget(Widget):
    name = 'group'

    def get_body(self):
        return self.content

    def generate_content(self, **kwargs):
        self.content = render_to_string('widgets/group.html',
                                        kwargs.get('context'))
