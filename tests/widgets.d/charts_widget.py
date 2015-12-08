from colab.widgets.widget_manager import WidgetManager
from colab.accounts.widgets.collaboration_chart import CollaborationChart
from colab.accounts.widgets.participation_chart import ParticipationChart

WidgetManager.register_widget('charts', CollaborationChart())
WidgetManager.register_widget('charts', ParticipationChart())
