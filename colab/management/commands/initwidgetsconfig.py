from django.core.management.base import BaseCommand


CONFIG_TEMPLATE = r"""
from colab.widgets.widget_manager import WidgetManager

from colab.super_archives.widgets.dashboard_latest_collaborations import \
    DashboardLatestCollaborationsWidget
from colab.super_archives.widgets.dashboard_most_relevant_threads import \
    DashboardMostRelevantThreadsWidget
from colab.super_archives.widgets.dashboard_latest_threads import \
    DashboardLatestThreadsWidget
from colab.super_archives.widgets.dashboard_collaboration_graph import \
    DashboardCollaborationGraphWidget

from colab.accounts.widgets.group import GroupWidget
from colab.accounts.widgets.group_membership import GroupMembershipWidget
from colab.accounts.widgets.latest_posted import LatestPostedWidget
from colab.accounts.widgets.latest_contributions import \
    LatestContributionsWidget

from colab.accounts.widgets.collaboration_chart import CollaborationChart
from colab.accounts.widgets.participation_chart import ParticipationChart

# Dashboard Widgets
WidgetManager.register_widget('dashboard',
                              DashboardLatestCollaborationsWidget())
WidgetManager.register_widget('dashboard',
                              DashboardCollaborationGraphWidget())
WidgetManager.register_widget('dashboard',
                              DashboardMostRelevantThreadsWidget())
WidgetManager.register_widget('dashboard',
                              DashboardLatestThreadsWidget())

# Profile Widgets
WidgetManager.register_widget('group', GroupWidget())
WidgetManager.register_widget('button', GroupMembershipWidget())
WidgetManager.register_widget('list', LatestPostedWidget())
WidgetManager.register_widget('list', LatestContributionsWidget())
WidgetManager.register_widget('charts', CollaborationChart())
WidgetManager.register_widget('charts', ParticipationChart())
"""


class Command(BaseCommand):
    help = ('Returns the default widget configuration, '
            'including the core widgets.')

    def handle(self, *args, **kwargs):
        print(CONFIG_TEMPLATE)
