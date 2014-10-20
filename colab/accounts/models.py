# -*- coding: utf-8 -*-

import urlparse

from django.db import models, DatabaseError
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from conversejs import xmpp

from .utils import mailman


class User(AbstractUser):
    institution = models.CharField(max_length=128, null=True, blank=True)
    role = models.CharField(max_length=128, null=True, blank=True)
    twitter = models.CharField(max_length=128, null=True, blank=True)
    facebook = models.CharField(max_length=128, null=True, blank=True)
    google_talk = models.EmailField(null=True, blank=True)
    github = models.CharField(max_length=128, null=True, blank=True,
                                 verbose_name=u'github')
    webpage = models.CharField(max_length=256, null=True, blank=True)
    verification_hash = models.CharField(max_length=32, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    bio = models.CharField(max_length=200, null=True, blank=True)

    def check_password(self, raw_password):

        if self.xmpp.exists() and raw_password == self.xmpp.first().password:
            return True

        return super(User, self).check_password(raw_password)

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'username': self.username})

    def twitter_link(self):
        return urlparse.urljoin('https://twitter.com', self.twitter)

    def facebook_link(self):
        return urlparse.urljoin('https://www.facebook.com', self.facebook)

    def mailinglists(self):
        return mailman.user_lists(self)

    def update_subscription(self, email, lists):
        mailman.update_subscription(email, lists)


# We need to have `email` field set as unique but Django does not
#   support field overriding (at least not until 1.6).
# The following workaroud allows to change email field to unique
#   without having to rewrite all AbstractUser here
User._meta.get_field('email')._unique = True
User._meta.get_field('username').help_text = _(
    u'Required. 30 characters or fewer. Letters, digits and '
    u'./+/-/_ only.'
)
User._meta.get_field('username').validators[0] = validators.RegexValidator(
    r'^[\w.+-]+$',
    _('Enter a valid username.'),
    'invalid'
)
