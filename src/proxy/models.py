# -*- coding: utf-8 -*-

from django.db import models


class Attachment(models.Model):
    type = models.TextField()
    filename = models.TextField()
    size = models.IntegerField(blank=True, null=True)
    time = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    author = models.TextField(blank=True)
    ipnr = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'attachment'


class Repository(models.Model):
    name = models.TextField()
    value = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'repository'


class Revision(models.Model):
    repos = models.IntegerField()
    rev = models.TextField()
    time = models.BigIntegerField(blank=True, null=True)
    author = models.TextField(blank=True)
    message = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'revision'


class Ticket(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.TextField(blank=True)
    time = models.BigIntegerField(blank=True, null=True)
    changetime = models.BigIntegerField(blank=True, null=True)
    component = models.TextField(blank=True)
    severity = models.TextField(blank=True)
    priority = models.TextField(blank=True)
    owner = models.TextField(blank=True)
    reporter = models.TextField(blank=True)
    cc = models.TextField(blank=True)
    version = models.TextField(blank=True)
    milestone = models.TextField(blank=True)
    status = models.TextField(blank=True)
    resolution = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    keywords = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'ticket'


class TicketChange(models.Model):
    ticket = models.IntegerField()
    time = models.BigIntegerField()
    author = models.TextField(blank=True)
    field = models.TextField()
    oldvalue = models.TextField(blank=True)
    newvalue = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'ticket_change'


class TicketCustom(models.Model):
    ticket = models.IntegerField()
    name = models.TextField()
    value = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'ticket_custom'


class Wiki(models.Model):
    name = models.TextField(primary_key=True)
    version = models.IntegerField()
    time = models.BigIntegerField(blank=True, null=True)
    author = models.TextField(blank=True)
    ipnr = models.TextField(blank=True)
    text = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    readonly = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wiki'

    def get_collaborators(self):
        return Wiki.objects.filter(
            name=self.name,
        ).values_list('author', flat=True)

    def get_author(self):
        return Wiki.objects.get(name=self.name, version=1).author
