
from django import template
import urllib
import urlparse


register = template.Library()


def append_to_get_parameter(path, query=None, **kwargs):
    query_dict = dict(urlparse.parse_qsl(query))
    for key, value in kwargs.items():
        query_dict[key] = value
    return u'{}?{}'.format(path, urllib.urlencode(query_dict))


def pop_from_get_parameter(path, query=None, **kwargs):
    query_dict = dict(urlparse.parse_qsl(query))
    for key, value in kwargs.items():
        if query_dict not in (key):
            continue
        if query_dict[key] == value:
            del query_dict[key]
            continue
        if value in query_dict[key]:
            aux = query_dict[key].split(value)
            query_dict[key] = u''.join(aux).strip()
    return u'{}?{}'.format(path, urllib.urlencode(query_dict))


@register.simple_tag(takes_context=True)
def append_to_get(context, **kwargs):
    return append_to_get_parameter(
        context['request'].META['PATH_INFO'],
        context['request'].META['QUERY_STRING'],
        **kwargs
    )


@register.simple_tag(takes_context=True)
def pop_from_get(context, **kwargs):
    return pop_from_get_parameter(
        context['request'].META['PATH_INFO'],
        context['request'].META['QUERY_STRING'],
        **kwargs
    )
