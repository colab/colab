from colab.widgets.widget_manager import WidgetManager
from colab.accounts.widgets.group_membership import GroupMembershipWidget
from colab.accounts.widgets.latest_posted import LatestPostedWidget
from colab.accounts.widgets.latest_contributions import LatestContributionsWidget
from colab.accounts.widgets.group import GroupWidget
# from colab.super_archives.widgets.dashboard_latest_collaborations import DashboardLatestCollaborationsWidget
# from colab.super_archives.widgets.dashboard_most_relevant_threads import DashboardMostRelevantThreadsWidget
# from colab.super_archives.widgets.dashboard_latest_threads import DashboardLatestThreadsWidget
# from colab.super_archives.widgets.dashboard_collaboration_graph import DashboardCollaborationGraphWidget


WidgetManager.register_widget('group', GroupWidget())
WidgetManager.register_widget('button', GroupMembershipWidget())
WidgetManager.register_widget('list', LatestPostedWidget())
WidgetManager.register_widget('list', LatestContributionsWidget())
# WidgetManager.register_widget(
#     'dashboard_latest_collaborations', DashboardLatestCollaborationsWidget())
# WidgetManager.register_widget(
#     'dashboard_most_relevant_threads', DashboardMostRelevantThreadsWidget())
# WidgetManager.register_widget(
#     'dashboard_latest_threads', DashboardLatestThreadsWidget())
# WidgetManager.register_widget(
#     'dashboard_collaboration_graph', DashboardCollaborationGraphWidget())
