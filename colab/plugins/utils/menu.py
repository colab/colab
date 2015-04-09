from django.core.urlresolvers import reverse_lazy


class ColabUrl(object):
    def __init__(self, display, url, auth):
        self.display = display
        self.url = url
        self.auth = auth


def colab_url_factory(namespace):

    def url(display, viewname, namespace=namespace, args=tuple(),
            kwargs={}, auth=False):

        if namespace:
            rev_viewname = ':'.join((namespace, viewname))
        else:
            rev_viewname = viewname

        url = reverse_lazy(rev_viewname, args=args, kwargs=kwargs)

        return ColabUrl(display, url, auth)

    return url
