
from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def gravatar(context, email, size=80):
    
    email_md5 = getattr(email, 'md5', 'anonymous')

    request = context.get('request')
    if getattr(request, 'is_secure'):
        protocol = 'https'
    else:
        protocol = 'http'

    return (u'<img src="{}://www.gravatar.com/avatar/{}?s={}&d=mm"'
            'height="{}px" width="{}px" />').format(protocol, email_md5,
                                                    size, size, size)
