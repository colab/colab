
import urlparse
import requests

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse


class User(AbstractUser):
    institution = models.CharField(max_length=128, null=True, blank=True)
    role = models.CharField(max_length=128, null=True, blank=True)
    twitter = models.CharField(max_length=128, null=True, blank=True)
    facebook = models.CharField(max_length=128, null=True, blank=True)
    google_talk = models.EmailField(null=True, blank=True)
    webpage = models.CharField(max_length=256, null=True, blank=True)
    verification_hash = models.CharField(max_length=32, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'username': self.username})

    def twitter_link(self):
        return urlparse.urljoin('https://twitter.com', self.twitter)

    def facebook_link(self):
        return urlparse.urljoin('https://www.facebook.com', self.facebook)

    def mailinglists(self, email=None):
        list_set = set()

        if not email:
            emails = self.emails.values_list('address', flat=True)
        else:
            emails = [email]

        for email in emails:
            try:
                lists = requests.get(settings.MAILMAN_API_URL, timeout=1,
                                     params={'address': email})
            except requests.exceptions.Timeout:
                pass
            list_set.update(lists.json())

        return tuple(list_set)


# We need to have `email` field set as unique but Django does not
#   support field overriding (at least not until 1.6).
# The following workaroud allows to change email field to unique
#   without having to rewrite all AbstractUser here
User._meta.get_field('email')._unique = True
