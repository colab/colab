
from django import template

from super_archives.models import EmailAddress


register = template.Library()


@register.simple_tag
def gravatar(email, size=80):
    if isinstance(email, basestring):
        try:
            email = EmailAddress.objects.get(address=email)
        except EmailAddress.DoesNotExist:
            pass

    email_md5 = getattr(email, 'md5', 'anonymous')

    return u'<img src="http://www.gravatar.com/avatar/{}?s={}&d=mm" height="{}px" width="{}px" />'.format(email_md5, size, size, size)
