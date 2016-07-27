# -*- coding: utf-8 -*-

import urlparse
from hashlib import md5

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from .signals import user_created, user_password_changed
from colab.accounts.utils import email


class ColabUserManager(UserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **kwargs):
        args = (username, email, password, is_staff, is_superuser)
        user = super(ColabUserManager, self)._create_user(*args, **kwargs)

        user_created.send(user.__class__, user=user, password=password)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):

        # It creates a valid password for users
        if not password:
            password = get_random_string()

        return super(ColabUserManager, self).create_user(username, email,
                                                         password,
                                                         **extra_fields)


class EmailAddressValidation(models.Model):
    address = models.EmailField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             related_name='emails_not_validated')
    validation_key = models.CharField(max_length=32, null=True,
                                      default=email.get_validation_key)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'address')

    @classmethod
    def create(cls, address, user):
        email_address_validation = cls.objects.create(address=address,
                                                      user=user)
        return email_address_validation

    @classmethod
    def verify_email(cls, email_address_validation, verification_url):
        return email.send_verification_email(
            email_address_validation.address,
            email_address_validation.user,
            email_address_validation.validation_key,
            verification_url
        )


class EmailAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                             related_name='emails', on_delete=models.SET_NULL)
    address = models.EmailField(unique=True)
    real_name = models.CharField(max_length=64, blank=True, db_index=True)
    md5 = models.CharField(max_length=32, null=True)

    class Meta:
        ordering = ('id', )

    def save(self, *args, **kwargs):
        self.md5 = md5(self.address).hexdigest()
        super(EmailAddress, self).save(*args, **kwargs)

    def get_full_name(self):
        if self.user and self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.real_name

    def get_full_name_or_anonymous(self):
        return self.get_full_name() or _('Anonymous')

    def __unicode__(self):
        return '"%s" <%s>' % (self.get_full_name(), self.address)


class User(AbstractUser):
    """
    For more information about AbstractUser
    @see: https://docs.djangoproject.com/en/1.7/ref/contrib/auth/
    """
    institution = models.CharField(max_length=128, null=True, blank=True)
    role = models.CharField(max_length=128, null=True, blank=True)
    # Twitter limits user name to 15 characters.
    twitter = models.CharField(max_length=15, null=True, blank=True)
    # Facebook limits user lenght to 15.
    facebook = models.CharField(max_length=15, null=True, blank=True)
    google_talk = models.EmailField(null=True, blank=True)
    github = models.CharField(max_length=39, null=True, blank=True,
                              verbose_name=u'github')
    webpage = models.CharField(max_length=256, null=True, blank=True)
    verification_hash = models.CharField(max_length=32, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    needs_update = models.BooleanField(default=True)

    objects = ColabUserManager()

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'username': self.username})

    def twitter_link(self):
        return urlparse.urljoin('https://twitter.com', self.twitter)

    def facebook_link(self):
        return urlparse.urljoin('https://www.facebook.com', self.facebook)

    def save(self, *args, **kwargs):

        # Forces username to be lowercase always
        self.username = self.username.lower()
        super(User, self).save(*args, **kwargs)

    def set_password(self, raw_password):
        super(User, self).set_password(raw_password)
        if self.pk:
            user_password_changed.send(User, user=self, password=raw_password)


# We need to have `email` field set as unique but Django does not
#   support field overriding (at least not until 1.6).
# The following workaroud allows to change email field to unique
#   without having to rewrite all AbstractUser here
User._meta.get_field('email')._unique = True
User._meta.get_field('username').help_text = _(
    u'Required. 30 characters or fewer. Letters and digits.'
)
