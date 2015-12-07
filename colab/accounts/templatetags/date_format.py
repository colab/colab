from django import template
from django.utils.translation import ugettext as _
register = template.Library()


@register.simple_tag(takes_context=True)
def date_format(context, date):
    formatted_date = _('%(m)s %(d)s %(y)s' % {'m': date.strftime('%B'),
                                              'd': date.day,
                                              'y': date.year})
    return formatted_date


@register.simple_tag(takes_context=True)
def datetime_format(context, date):
    formatted_date = date_format(context, date)
    formatted_time = _('%(hour)s:%(min)s' % {'hour': date.hour,
                                             'min': date.strftime('%I')})
    formatted_datetime = _('%s at %s' % (formatted_date, formatted_time))
    return formatted_datetime
