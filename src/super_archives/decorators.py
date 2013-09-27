
from django.core.cache import cache

from super_archives.models import PageHit


def count_hit(view):
    def wrapper(request, *args, **kwargs):
        # Here we cache the user's IP to ensure that the same
        #   IP won't hit the same page again for while
        ip_addr = request.META.get('REMOTE_ADDR')
        cache_key = u'page_hits-{}-{}'.format(request.path_info, ip_addr)
        duplicate = cache.get(cache_key)
        if duplicate:
            return view(request, *args, **kwargs)
        cache.set(cache_key, True)

        # Everything ok, so just increment the page count
        page_hit = PageHit.objects.get_or_create(url_path=request.path_info)[0]
        page_hit.hit_count += 1
        page_hit.save()

        return view(request, *args, **kwargs)
    return wrapper
