
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
    menu = ''
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

        items = ''

        for text, link in links:
            url = reverse(app.label, args=(link,))
            items += PROXY_MENU_ITEM_TEMPLATE.format(link=url,
                                                     link_title=unicode(text))
        menu += PROXY_MENU_TEMPLATE.format(title=unicode(title), items=items)

    return menu
