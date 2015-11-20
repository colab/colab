from django import template
from colab.search.utils import url


register = template.Library()


@register.simple_tag(takes_context=True)
def append_to_get(context, **kwargs):
    return url.append_to_get(
        context['request'].META['PATH_INFO'],
        context['request'].META['QUERY_STRING'],
        **kwargs
    )


@register.simple_tag(takes_context=True)
def pop_from_get(context, **kwargs):
    return url.pop_from_get(
        context['request'].META['PATH_INFO'],
        context['request'].META['QUERY_STRING'],
        **kwargs
    )
