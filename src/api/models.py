# -*- coding: utf-8 -*-

from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.resources import ModelResource

from accounts.models import User
from super_archives.models import Message, EmailAddress
from proxy.models import Revision, Ticket, Wiki


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.filter(is_active=True)
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff',
                    'is_superuser', 'verification_hash']
        allowed_methods = ['get', ]
        filtering = {
            'username': ALL,
            'institution': ALL,
            'role': ALL,
            'twitter': ALL,
            'facebook': ALL,
            'google_talk': ALL,
            'github': ALL,
            'webpage': ALL,
            'bio': ALL,
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(UserResource, self).build_filters(filters)

        if 'email' in filters:
            qs = User.objects.filter(email=filters['email'])
            orm_filters['pk__in'] = [i.pk for i in qs]

        return orm_filters


class EmailAddressResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=False, null=True)

    class Meta:
        queryset = EmailAddress.objects.all()
        resource_name = 'emailaddress'
        excludes = ['address', 'md5']
        allowed_methods = ['get', ]
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'real_name': ALL,
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(EmailAddressResource, self).build_filters(filters)

        if 'email' in filters or 'address' in filters:
            address = filters.get('email') if filters.get('email') else \
                    filters.get('address')
            qs = EmailAddress.objects.filter(address=address)
            orm_filters['pk__in'] = [i.pk for i in qs]

        return orm_filters


class MessageResource(ModelResource):
    emailaddress = fields.ForeignKey(EmailAddressResource, 'from_address',
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
