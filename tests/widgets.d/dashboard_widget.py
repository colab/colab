from colab.widgets.widget_manager import WidgetManager
from colab.widgets.dashboard.dashboard_latest_collaborations import DashboardLatestCollaborationsWidget
from colab.widgets.dashboard.dashboard_collaboration_graph import DashboardCollaborationGraphWidget


WidgetManager.register_widget(
    'dashboard', DashboardLatestCollaborationsWidget())
WidgetManager.register_widget(
    'dashboard', DashboardCollaborationGraphWidget())
