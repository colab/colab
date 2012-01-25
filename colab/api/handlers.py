
from django.core.cache import cache
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from piston.utils import rc
from piston.handler import BaseHandler

from colab.super_archives.models import Message, PageHit


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


class CountHandler(BaseHandler):
    allowed_methods = ('POST')

    def create(self, request):
        """Add one page view for the given url"""
        
        # If missing the path_info argument we can't do anything
        path_info = request.POST.get('path_info')
        if not path_info:
            return rc.BAD_REQUEST

        # Here we cache the user's IP to ensure that the same
        #   IP won't hit the same page again for while
        ip_addr = request.META.get('REMOTE_ADDR')
        page_hits_cache = cache.get('page_hits', {})
        duplicate = page_hits_cache.get(path_info, {}).get(ip_addr)
        
        if duplicate:
            return rc.DUPLICATE_ENTRY
        else:
            page_hits_cache.update({path_info: {ip_addr: True }})
            cache.set('page_hits', page_hits_cache)
        
        # Everything ok, so just increment the page count
        page_hit = PageHit.objects.get_or_create(url_path=path_info)[0]
        page_hit.hit_count += 1
        page_hit.save()
        
        return rc.CREATED

