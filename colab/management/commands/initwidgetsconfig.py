from django.core.management.base import BaseCommand


CONFIG_TEMPLATE = r"""
from colab.widgets.widget_manager import WidgetManager

from colab.widgets.dashboard.dashboard_latest_collaborations import \
    DashboardLatestCollaborationsWidget
from colab.widgets.dashboard.dashboard_collaboration_graph import \
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
"""


class Command(BaseCommand):
    help = ('Returns the default widget configuration, '
            'including the core widgets.')

    def handle(self, *args, **kwargs):
        print(CONFIG_TEMPLATE)
