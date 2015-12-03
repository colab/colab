from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class Widget(object):
    identifier = None
    name = None
    content = ''
    template = ''

    def get_body(self):
        # avoiding regex in favor of performance
        start = self.content.find('<body>')
        end = self.content.find('</body>')

        if -1 in [start, end]:
            return ''

        body = self.content[start + len('<body>'):end]
        return mark_safe(body)

    def get_header(self):
        # avoiding regex in favor of performance
        start = self.content.find('<head>')
        end = self.content.find('</head>')

        if -1 in [start, end]:
            return ''

        head = self.content[start + len('<head>'):end]
        return mark_safe(head)

    def generate_content(self, **kwargs):
        if not self.template:
            class_name = self.__class__.__name__
            raise Exception("Template not defined in {}.".format(class_name))
        self.content = render_to_string(self.template, kwargs.get('context'))


class WidgetManager(object):
    widget_categories = {}

    @staticmethod
    def register_widget(category, widget):
        if category not in WidgetManager.widget_categories:
            WidgetManager.widget_categories[category] = []

        WidgetManager.widget_categories[category].append(widget)

    @staticmethod
    def unregister_widget(category, widget_identifier):
        if category in WidgetManager.widget_categories:
            for widget in WidgetManager.widget_categories[category]:
                if widget.identifier == widget_identifier:
                    WidgetManager.widget_categories[category].remove(widget)

    @staticmethod
    def get_widgets(category, **kwargs):
        if category not in WidgetManager.widget_categories:
            return []

        widgets = WidgetManager.widget_categories[category][:]
        for widget in widgets:
            widget.generate_content(**kwargs)
        return widgets
