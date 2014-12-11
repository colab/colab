from django.db import models
from django.conf import settings
from colab.accounts.models import User

class GitlabProject(models.Model):

    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    public = models.BooleanField(default=True)
    name = models.TextField()
    name_with_namespace = models.TextField()
    created_at = models.DateTimeField(blank=True)
    last_activity_at = models.DateTimeField(blank=True)
