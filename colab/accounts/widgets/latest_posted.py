from colab.widgets.widget_manager import Widget


class LatestPostedWidget(Widget):
    name = 'last posted'
    template = 'widgets/latest_posted.html'
