# -*- coding: utf-8 -*-

from django import template

from super_archives.utils import url

register = template.Library()


@register.simple_tag(takes_context=True)
def append_to_get(context, **kwargs):
    return url.append_to_get(
        context['request'].META['PATH_INFO'],
        context['request'].META['QUERY_STRING'],
        **kwargs
    )
