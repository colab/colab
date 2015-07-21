from colab.plugins.utils.models import Collaboration
from django.db import models
from django.utils.translation import ugettext_lazy as _


class NoosferoCategory(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{}-{}".format(self.id, self.name)


class NoosferoCommunity(Collaboration):

    id = models.IntegerField(primary_key=True)
    type = u'community'
    icon_name = u'file'
    name = models.TextField()
    identifier = models.TextField()
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(NoosferoCategory)
    created_at = models.DateTimeField(blank=True)

    @property
    def url(self):
        return u'/social/profile/{}'.format(self.identifier)

    @property
    def modified(self):
        return self.created_at

    def __unicode__(self):
        return "{}({}) - {}".format(self.name, self.identifier,
                                    self.description)

    class Meta:
        verbose_name = _('Community')
        verbose_name_plural = _('Communities')


class NoosferoArticle(Collaboration):

    id = models.IntegerField(primary_key=True)
    type = u'article'
    icon_name = u'file'
    title = models.TextField()
    path = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(NoosferoCategory)
    profile_identifier = models.TextField()
    created_at = models.DateTimeField(blank=True)

    @property
    def url(self):
        return u'/social/{}/{}'.format(self.profile_identifier, self.path)

    @property
    def modified(self):
        return self.created_at

    def __unicode__(self):
        return "{}({})".format(self.title, self.path)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
