from colab.widgets.widget_manager import WidgetManager
from colab.accounts.widgets.group import GroupWidget
from colab.accounts.widgets.group_membership import GroupMembershipWidget
from colab.accounts.widgets.latest_posted import LatestPostedWidget
from colab.accounts.widgets.latest_contributions import LatestContributionsWidget


WidgetManager.register_widget('group', GroupWidget())
WidgetManager.register_widget('button', GroupMembershipWidget())
WidgetManager.register_widget('list', LatestPostedWidget())
WidgetManager.register_widget('list', LatestContributionsWidget())
