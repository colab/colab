
from django.core.urlresolvers import reverse
from django import template
from django.core.cache import cache
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(takes_context=True)
def proxy_menu(context):
    if context['user'].is_authenticated():
        cache_key = 'colab-proxy-menu-authenticated'
    else:
        cache_key = 'colab-proxy-menu-anonymous'

    menu_from_cache = cache.get(cache_key)

    if menu_from_cache:
        return menu_from_cache

    menu_links = {}
    proxied_apps = context.get('proxy', {})

    for app in proxied_apps.values():
        if not hasattr(app, 'menu'):
            continue

        title = app.menu.get('title', app.label.title())
        links = app.menu.get('links', tuple())
        if context['user'].is_active:
            links += app.menu.get('auth_links', tuple())

        if not links:
            continue

        if title not in menu_links:
            menu_links[title] = []

        for text, link in links:
            url = reverse(app.label, args=(link,))
            menu_links[title].append((text, url))

    menu = render_to_string('proxy/menu_template.html',
                            {'menu_links': menu_links})

    cache.set(cache_key, menu)
    return menu
