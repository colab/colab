from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def set(context, var_name, var_value):
    context[var_name] = var_value
    return ""
