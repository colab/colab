
from django import http
from django.db import IntegrityError
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist


from super_archives.models import Message


class VoteView(View):

    http_method_names = [u'get', u'put', u'delete', u'head']

    def put(self, request, msg_id):
        if not request.user.is_authenticated():
            return http.HttpResponseForbidden()

        try:
            Message.objects.get(id=msg_id).vote(request.user)
        except IntegrityError:
            # 409 Conflict
            #   used for duplicated entries
            return http.HttpResponse(status=409)

        # 201 Created
        return http.HttpResponse(status=201)

    def get(self, request, msg_id):
        votes = Message.objects.get(id=msg_id).votes_count()
        return http.HttpResponse(votes, content_type='application/json')

    def delete(self, request, msg_id):
        if not request.user.is_authenticated():
            return http.HttpResponseForbidden()

        try:
            Message.objects.get(id=msg_id).unvote(request.user)
        except ObjectDoesNotExist:
            return http.HttpResponseGone()

        # 204 No Content
        #   empty body, as per RFC2616.
        #   object deleted
        return http.HttpResponse(status=204)
