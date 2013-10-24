
from django.db import models
from django.core.cache import cache
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class Hit(models.Model):
    created = models.DateField(auto_now_add=True, db_index=True)
    updated = models.DateField(auto_now=True, db_index=True)
    hits = models.PositiveIntegerField(default=0)
    content_type = models.ForeignKey(ContentType)
    object_pk = models.CharField(max_length=256)

    class Meta:
        unique_together = ('content_type', 'object_pk')


class HitCountModelMixin(object):

    @property
    def hits(self):
        content_type = ContentType.objects.get_for_model(self.__class__,
                                                         for_concrete_model=False)
        try:
            hit = Hit.objects.get(content_type=content_type,
                                  object_pk=self.pk)
        except Hit.DoesNotExist:
            return 0

        return hit.hits

    def hit(self, request=None):
        content_type = ContentType.objects.get_for_model(self.__class__)

        # Here we cache the user's IP to ensure that the same
        #   IP won't hit the same page again for while
        if request:
            ip_addr = request.META.get('REMOTE_ADDR')
            cache_key = u'page_hits-{}-{}-{}'.format(ip_addr,
                                                     content_type, self.pk)
            duplicate = cache.get(cache_key)
            if duplicate:
                return
            cache.set(cache_key, True)

        # Everything ok, so just increment the page count
        hit_ = Hit.objects.get_or_create(content_type=content_type,
                                         object_pk=self.pk)[0]
        hit_.hits += 1
        hit_.save()
