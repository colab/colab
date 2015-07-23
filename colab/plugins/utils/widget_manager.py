
class Widget:
    identifier = None
    name = None
    default_url = None
    content = None

    def get_body(self):
        # avoiding regex in favor of performance
        start = content.find('<body>')
        end = content.find('</body>')
        head = content[start + len('<body>'):end]
        return head

    def get_header(self):
        # avoiding regex in favor of performance
        start = content.find('<head>')
        end = content.find('</head>')
        head = content[start + len('<head>'):end]
        return head

    def generate_content(self, request=None):
        self.content = ''


class WidgetManager(object):
    widget_categories = {}

    @staticmethod
    def register_widget(category, widget):
        if not WidgetManager.widget_categories.has_key(category):
            WidgetManager.widget_categories[category] = []

        WidgetManager.widget_categories[category].append(widget)

    @staticmethod
    def get_widgets(category, request=None):
        if not WidgetManager.widget_categories.has_key(category):
            return []

        widgets = WidgetManager.widget_categories[category]
        for widget in widgets:
            widget.generate_content(request)
        return widgets
