
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from piston.utils import rc
from piston.handler import BaseHandler

from super_archives.models import Message


class VoteHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'DELETE')

    def create(self, request, message_id):
        if not request.user.is_authenticated():
            return rc.FORBIDDEN
        
        try:
            Message.objects.get(id=message_id).vote(request.user)
        except IntegrityError:
            return rc.DUPLICATE_ENTRY

        return rc.CREATED
    
    def read(self, request, message_id):
        return Message.objects.get(id=message_id).votes_count()
        
    def delete(self, request, message_id):
        if not request.user.is_authenticated():
            return rc.FORBIDDEN
        
        try:
            Message.objects.get(id=message_id).unvote(request.user)
        except ObjectDoesNotExist:
            return rc.NOT_HERE
            
        return rc.DELETED


        

