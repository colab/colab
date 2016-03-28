from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class Widget(object):
    identifier = None
    name = None
    content = ''
    template = ''
    bootstrap_conflict = False
    jquery_conflict = False

    def get_body(self):
        start = self.content.find('<body')
        start = self.content.find('>', start)
        end = self.content.find('</body>')

        if -1 in [start, end]:
            return self.content

        # 1 correspond to string size of '>'
        body = self.content[start + 1:end]
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
    bootstrap_conflict = False
    jquery_conflict = False

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

            if not WidgetManager.bootstrap_conflict and \
               widget.bootstrap_conflict:
                WidgetManager.bootstrap_conflict = True

            if not WidgetManager.jquery_conflict and \
               widget.jquery_conflict:
                WidgetManager.jquery_conflict = True

        return widgets
