
from django import template
from colab.super_archives.utils import url


register = template.Library()
TEMPLATE_PATH = 'superarchives/tags/'


@register.inclusion_tag(TEMPLATE_PATH + 'display_message.html')
def display_message(email):
    if not email.blocks.count():
        email.update_blocks()

    return {'blocks': email.blocks.all}


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


@register.assignment_tag()
def profile_url(username, user_url):
    if not username or not user_url:
        return ""

    return '- <a href="%s">%s</a>' % (user_url, username)
