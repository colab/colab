# -*- coding: utf-8 -*-

import urlparse

from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse

from conversejs import xmpp

from .utils import mailman


class User(AbstractUser):
    institution = models.CharField(max_length=128, null=True, blank=True)
    role = models.CharField(max_length=128, null=True, blank=True)
    twitter = models.CharField(max_length=128, null=True, blank=True)
    facebook = models.CharField(max_length=128, null=True, blank=True)
    google_talk = models.EmailField(null=True, blank=True)
    webpage = models.CharField(max_length=256, null=True, blank=True)
    verification_hash = models.CharField(max_length=32, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    def check_password(raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        if not raw_password or not self.has_usable_password():
            return False
        return self.password == raw_password

    def set_password(self, raw_password):
        self.password = unicode(raw_password)

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


def password_change(sender, instance, **kwargs):
    from conversejs.models import XMPPAccount
    # to register an XMPPAccount for an user, do the following:
    # xmpp.register_account('username@domain', 'user_password'
    #                       'name', 'email')
    # the domain can be found at conversejs.conf.CONVERSEJS_AUTO_REGISTER

    try:
        user = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return # should I register a xmpp account here?

    try:
        xmpp_account = XMPPAccount.objects.get(user=instance.pk)
    except XMPPAccount.DoesNotExist:
        return # User's XMPP account should be created here?

    if user.password != instance.password:
        xmpp.change_password(xmpp_account, instance.password)


pre_save.connect(password_change, sender=User)
