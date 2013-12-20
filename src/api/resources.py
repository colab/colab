# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.resources import ModelResource

from super_archives.models import Message, EmailAddress
from proxy.models import Revision, Ticket, Wiki


User = get_user_model()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.filter(is_active=True)
        resource_name = 'user'
        fields = ['username', 'institution', 'role', 'bio', 'first_name',
                  'last_name', 'email']
        allowed_methods = ['get', ]
        filtering = {
            'email': ('exact', ),
            'username': ALL,
            'institution': ALL,
            'role': ALL,
            'bio': ALL,
        }

    def dehydrate_email(self, bundle):
        return ''


class EmailAddressResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=False, null=True)

    class Meta:
        queryset = EmailAddress.objects.all()
        resource_name = 'emailaddress'
        excludes = ['md5', ]
        allowed_methods = ['get', ]
        filtering = {
            'address': ('exact', ),
            'user': ALL_WITH_RELATIONS,
            'real_name': ALL,
        }

    def dehydrate_address(self, bundle):
        return ''


class MessageResource(ModelResource):
    from_address = fields.ForeignKey(EmailAddressResource, 'from_address',
                                     full=False)

    class Meta:
        queryset = Message.objects.all()
        resource_name = 'message'
        excludes = ['spam', 'subject_clean', 'message_id']
        filtering = {
            'from_address': ALL_WITH_RELATIONS,
            'subject': ALL,
            'body': ALL,
            'received_time': ALL,
        }


class RevisionResource(ModelResource):
    class Meta:
        queryset = Revision.objects.all()
        resource_name = 'revision'
        excludes = ['collaborators', ]
        filtering = {
            'key': ALL,
            'rev': ALL,
            'author': ALL,
            'message': ALL,
            'repository_name': ALL,
            'created': ALL,
        }


class TicketResource(ModelResource):
    class Meta:
        queryset = Ticket.objects.all()
        resource_name = 'ticket'
        excludes = ['collaborators', ]
        filtering = {
            'id': ALL,
            'summary': ALL,
            'description': ALL,
            'milestone': ALL,
            'priority': ALL,
            'component': ALL,
            'version': ALL,
            'severity': ALL,
            'reporter': ALL,
            'author': ALL,
            'status': ALL,
            'keywords': ALL,
            'created': ALL,
            'modified': ALL,
            'modified_by': ALL,
        }


class WikiResource(ModelResource):
    class Meta:
        queryset = Wiki.objects.all()
        resource_name = 'wiki'
        excludes = ['collaborators', ]
        filtering = {
            'name': ALL,
            'wiki_text': ALL,
            'author': ALL,
            'name': ALL,
            'created': ALL,
            'modified': ALL,
            'modified_by': ALL,
        }
