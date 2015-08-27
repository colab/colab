from collections import OrderedDict

from django import template
from django.core.cache import cache
from django.template.loader import render_to_string
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag(takes_context=True)
def plugins_menu(context):

    if context['user'].is_authenticated():
        cache_key = 'colab-plugin-menu-authenticated'
    else:
        cache_key = 'colab-plugin-menu-anonymous'

    lang = get_language()
    cache_key += '-{}'.format(lang)

    menu_from_cache = cache.get(cache_key)

    if menu_from_cache:
        return menu_from_cache

    menu_links = OrderedDict()
    colab_apps = context.get('plugins', {})

    for app_name, app in colab_apps.items():
        if not app.get('menu_urls'):
            continue

        menu = app.get('menu_urls')
        title = app.get('menu_title', app_name)

        if title not in menu_links:
            menu_links[title] = []

        for colab_url in menu:
            if not context['user'].is_active and colab_url.auth:
                continue

            menu_links[title].append(colab_url)

        if not menu_links[title]:
            del menu_links[title]

    menu = render_to_string('plugins/menu_template.html',
                            {'menu_links': menu_links})

    cache.set(cache_key, menu)
    return menu
