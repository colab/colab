# -*- coding: utf-8 -*-
import os
import urllib2

from django.db import models
from django.conf import settings

from hitcounter.models import HitCounterModelMixin

from colab.accounts.models import User


class Attachment(models.Model, HitCounterModelMixin):
    url = models.TextField(primary_key=True)
    attach_id = models.TextField()
    used_by = models.TextField()
    filename = models.TextField()
    author = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(blank=True)
    mimetype = models.TextField(blank=True)
    size = models.IntegerField(blank=True)

    class Meta:
        managed = False
        db_table = 'attachment_view'

    @property
    def filepath(self):
        return os.path.join(
            settings.ATTACHMENTS_FOLDER_PATH,
            self.used_by,
            self.attach_id,
            urllib2.quote(self.filename.encode('utf8'))
        )

    def get_absolute_url(self):
        return u'/raw-attachment/{}'.format(self.url)

    def get_author(self):
        try:
            return User.objects.get(username=self.author)
        except User.DoesNotExist:
            return None


class Revision(models.Model, HitCounterModelMixin):
    key = models.TextField(blank=True, primary_key=True)
    rev = models.TextField(blank=True)
    author = models.TextField(blank=True)
    message = models.TextField(blank=True)
    repository_name = models.TextField(blank=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'revision_view'

    def get_absolute_url(self):
        return u'/changeset/{}/{}'.format(self.rev, self.repository_name)

    def get_author(self):
        try:
            return User.objects.get(username=self.author)
        except User.DoesNotExist:
            return None


class Ticket(models.Model, HitCounterModelMixin):
    id = models.IntegerField(primary_key=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    milestone = models.TextField(blank=True)
    priority = models.TextField(blank=True)
    component = models.TextField(blank=True)
    version = models.TextField(blank=True)
    severity = models.TextField(blank=True)
    reporter = models.TextField(blank=True)
    author = models.TextField(blank=True)
    status = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    collaborators = models.TextField(blank=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    modified_by = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'ticket_view'

    def get_absolute_url(self):
        return u'/ticket/{}'.format(self.id)

    def get_author(self):
        try:
            return User.objects.get(username=self.author)
        except User.DoesNotExist:
            return None

    def get_modified_by(self):
        try:
            return User.objects.get(username=self.modified_by)
        except User.DoesNotExist:
            return None


class Wiki(models.Model, HitCounterModelMixin):
    name = models.TextField(primary_key=True)
    wiki_text = models.TextField(blank=True)
    author = models.TextField(blank=True)
    collaborators = models.TextField(blank=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    modified_by = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'wiki_view'

    def get_absolute_url(self):
        return u'/wiki/{}'.format(self.name)

    def get_author(self):
        try:
            return User.objects.get(username=self.author)
        except User.DoesNotExist:
            return None

    def get_modified_by(self):
        try:
            return User.objects.get(username=self.modified_by)
        except User.DoesNotExist:
            return None


class WikiCollabCount(models.Model):
    author = models.TextField(primary_key=True)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wiki_collab_count_view'


class TicketCollabCount(models.Model):
    author = models.TextField(primary_key=True)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ticket_collab_count_view'
