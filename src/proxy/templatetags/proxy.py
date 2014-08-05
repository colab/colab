from django import template

from super_archives.utils import url
from django.conf import settings


register = template.Library()
TEMPLATE_PATH = 'proxy/tags/'

@register.assignment_tag
def is_trac_enable():
    return settings.TRAC_ENABLED