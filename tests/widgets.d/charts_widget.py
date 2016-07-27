from colab.widgets.widget_manager import WidgetManager
from colab.accounts.widgets.collaboration_chart import CollaborationChart

WidgetManager.register_widget('charts', CollaborationChart())
