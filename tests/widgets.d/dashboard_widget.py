from colab.widgets.widget_manager import WidgetManager
from colab.super_archives.widgets.dashboard_latest_collaborations import DashboardLatestCollaborationsWidget
from colab.super_archives.widgets.dashboard_most_relevant_threads import DashboardMostRelevantThreadsWidget
from colab.super_archives.widgets.dashboard_latest_threads import DashboardLatestThreadsWidget
from colab.super_archives.widgets.dashboard_collaboration_graph import DashboardCollaborationGraphWidget


WidgetManager.register_widget(
    'dashboard', DashboardLatestCollaborationsWidget())
WidgetManager.register_widget(
    'dashboard', DashboardCollaborationGraphWidget())
WidgetManager.register_widget(
    'dashboard', DashboardMostRelevantThreadsWidget())
WidgetManager.register_widget(
    'dashboard', DashboardLatestThreadsWidget())
