
from django import template

register = template.Library()


@register.inclusion_tag('tz/set_utc_offset.html')
def utc_offset_cookie():
    return
