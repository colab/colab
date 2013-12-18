# -*- coding: utf-8 -*-

from tastypie import fields
from tastypie.resources import ModelResource

from accounts.models import User
from super_archives.models import Message
from proxy.models import Revision, Ticket, Wiki


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.filter(is_active=True)
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff',
                    'is_superuser', 'verification_hash']
        allowed_methods = ['get', ]


class MessageResource(ModelResource):
    class Meta:
        queryset = Message.objects.all()
        resource_name = 'message'
        excludes = ['spam', 'subject_clean', 'message_id']


class RevisionResource(ModelResource):
    class Meta:
        queryset = Revision.objects.all()
        resource_name = 'revision'
        excludes = ['collaborators', ]


class TicketResource(ModelResource):
    class Meta:
        queryset = Ticket.objects.all()
        resource_name = 'ticket'
        excludes = ['collaborators', ]


class WikiResource(ModelResource):
    class Meta:
        queryset = Wiki.objects.all()
        resource_name = 'wiki'
        excludes = ['collaborators', ]
