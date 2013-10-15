
from django import template


register = template.Library()
TEMPLATE_PATH = 'superarchives/tags/'


@register.inclusion_tag(TEMPLATE_PATH + 'display_message.html')
def display_message(email):
    return {'blocks': email.blocks()}
