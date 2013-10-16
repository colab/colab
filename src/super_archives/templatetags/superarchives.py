
from django import template


register = template.Library()
TEMPLATE_PATH = 'superarchives/tags/'


@register.inclusion_tag(TEMPLATE_PATH + 'display_message.html')
def display_message(email):
    if not email.blocks.count():
        email.update_blocks()

    return { 'blocks': email.blocks.all }
