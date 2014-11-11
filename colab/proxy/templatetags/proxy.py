
from django.core.urlresolvers import reverse
from django import template

register = template.Library()

PROXY_MENU_TEMPLATE = """
<li class="dropdown">
  <a href="#" class="dropdown-toggle" data-toggle="dropdown">{title}
                                                    <b class="caret"></b></a>
  <ul class="dropdown-menu">
    {items}
  </ul>
</li>"""

PROXY_MENU_ITEM_TEMPLATE = """
    <li><a href="{link}">{link_title}</a></li>
"""


@register.simple_tag(takes_context=True)
def proxy_menu(context):
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

    menu = ''

    for title, links in menu_links.items():
        items = ''
        for text, link in links:
            items += PROXY_MENU_ITEM_TEMPLATE.format(link=link,
                                                     link_title=unicode(text))
        menu += PROXY_MENU_TEMPLATE.format(title=unicode(title), items=items)

    return menu
