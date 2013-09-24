
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    institution = models.CharField(max_length=128, null=True)
    role = models.CharField(max_length=128, null=True)
    twitter = models.CharField(max_length=128, null=True)
    facebook = models.CharField(max_length=128, null=True)
    google_talk = models.EmailField(null=True)
    webpage = models.CharField(max_length=256, null=True)
    verification_hash = models.CharField(max_length=32, null=True)

# We need to have `email` field set as unique but Django does not
#   support field overriding (at least not until 1.6).
# The following workaroud allows to change email field to unique
#   without having to rewrite all AbstractUser here
User._meta.get_field('email')._unique = True
