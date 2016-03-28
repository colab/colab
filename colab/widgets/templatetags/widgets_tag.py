from django import template
from colab.widgets.widget_manager import WidgetManager


register = template.Library()


@register.simple_tag(takes_context=True)
def import_widgets(context, area_id, widget_var=None):
    if not widget_var:
        widget_var = "widgets_{}".format(area_id)

    context[widget_var] = WidgetManager.get_widgets(area_id, context=context)
    context['bootstrap_conflict'] = WidgetManager.bootstrap_conflict
    context['jquery_conflict'] = WidgetManager.jquery_conflict

    return ""
