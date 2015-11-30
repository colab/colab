from colab.widgets.widget_manager import Widget


class DashboardLatestThreadsWidget(Widget):
    name = 'latest threads'
    template = 'widgets/dashboard_latest_threads.html'
