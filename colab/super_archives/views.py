# -*- coding: utf-8 -*-

import smtplib
import logging
import urlparse

import requests

from django import http
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.views.generic import View, ListView
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from colab.accounts.utils import mailman
from colab.accounts.models import User
from .utils.email import send_verification_email
from .models import (MailingList, Thread, EmailAddress,
                     EmailAddressValidation, Message)


class ThreadView(View):
    http_method_names = [u'get', u'post']

    def get(self, request, mailinglist, thread_token):

        thread = get_object_or_404(Thread, subject_token=thread_token,
                                   mailinglist__name=mailinglist)

        all_privates = []
        all_privates.extend(
            [mlist.get('listname')
                for mlist in mailman.all_lists()
                if mlist.get('archive_private')]
        )

        if all_privates.count(thread.mailinglist.name):
            if not request.user.is_authenticated():
                raise PermissionDenied
            else:
                user = User.objects.get(username=request.user)
                emails = user.emails.values_list('address', flat=True)
                lists_for_user = mailman.get_user_mailinglists(user)
                listnames_for_user = mailman.extract_listname_from_list(
                    lists_for_user)
                if thread.mailinglist.name not in listnames_for_user:
                    raise PermissionDenied

        thread.hit(request)

        try:
            first_message = thread.message_set.first()
        except ObjectDoesNotExist:
            raise http.Http404

        order_by = request.GET.get('order')
        if order_by == 'voted':
            msgs_query = Message.most_voted
        else:
            msgs_query = Message.objects

        msgs_query = msgs_query.filter(thread__subject_token=thread_token)
        msgs_query = msgs_query.filter(thread__mailinglist__name=mailinglist)
        emails = msgs_query.exclude(id=first_message.id)

        total_votes = first_message.votes_count()
        for email in emails:
            total_votes += email.votes_count()

        # Update relevance score
        thread.update_score()

        context = {
            'first_msg': first_message,
            'emails': [first_message] + list(emails),
            'pagehits': thread.hits,
            'total_votes': total_votes,
            'thread': thread,
        }

        return render(request, 'message-thread.html', context)

    def post(self, request, mailinglist, thread_token):
        try:
            thread = Thread.objects.get(subject_token=thread_token,
                                        mailinglist__name=mailinglist)
        except Thread.DoesNotExist:
            raise http.Http404

        data = {
            'in_reply_to': thread.message_set.last().message_id,
            'email_from': request.user.email,
            'name_from': request.user.get_full_name(),
            'subject': thread.message_set.first().subject_clean,
            'body': request.POST.get('emailbody', '').strip(),
        }

        url = urlparse.urljoin(settings.MAILMAN_API_URL,
                               'sendmail/' + mailinglist)

        error_msg = None
        try:
            resp = requests.post(url, data=data, timeout=2)
        except requests.exceptions.ConnectionError:
            resp = None
            error_msg = _('Error trying to connect to Mailman API')
        except requests.exceptions.Timeout:
            resp = None
            error_msg = _('Timeout trying to connect to Mailman API')

        if resp and resp.status_code == 200:
            messages.success(request, _(
                "Your message was sent to this topic. "
                "It may take some minutes before it's delivered by email "
                "to the group. Why don't you breath some fresh air in the "
                "meanwhile?"
            ))
        else:
            if not error_msg:
                if resp is not None:
                    if resp.status_code == 400:
                        error_msg = _('You cannot send an empty email')
                    elif resp.status_code == 404:
                        error_msg = _('Mailing list does not exist')
                else:
                    error_msg = \
                        _('Unknown error trying to connect to Mailman API')

            messages.error(request, error_msg)

        return self.get(request, mailinglist, thread_token)


class ThreadDashboardView(ListView):
    http_method_names = ['get']
    context_object_name = 'lists'
    template_name = 'superarchives/thread-dashboard.html'
    paginate_by = 10

    def get_queryset(self):
        listnames_for_user = []
        if self.request.user.is_authenticated():
            user = User.objects.get(username=self.request.user)
            lists_for_user = mailman.get_user_mailinglists(user)
            listnames_for_user = mailman.extract_listname_from_list(
                lists_for_user)

        query = Q(is_private=False) | Q(name__in=listnames_for_user)

        return MailingList.objects.filter(query).order_by('name')


class EmailView(View):

    http_method_names = [u'head', u'get', u'post', u'delete', u'update']

    def get(self, request, key):
        """Validate an email with the given key"""

        try:
            email_val = EmailAddressValidation.objects.get(validation_key=key)
        except EmailAddressValidation.DoesNotExist:
            messages.error(request, _('The email address you are trying to '
                                      'verify either has already been verified'
                                      ' or does not exist.'))
            return redirect('/')

        try:
            email = EmailAddress.objects.get(address=email_val.address)
        except EmailAddress.DoesNotExist:
            email = EmailAddress(address=email_val.address)

        if email.user and email.user.is_active:
            messages.error(request, _('The email address you are trying to '
                                      'verify is already an active email '
                                      'address.'))
            email_val.delete()
            return redirect('/')

        email.user = email_val.user
        email.save()
        email_val.delete()

        user = User.objects.get(username=email.user.username)
        user.is_active = True
        user.save()

        messages.success(request, _('Email address verified!'))
        return redirect('user_profile', username=email_val.user.username)

    @method_decorator(login_required)
    def post(self, request, key):
        """Create new email address that will wait for validation"""

        email = request.POST.get('email')
        user_id = request.POST.get('user')
        if not email:
            return http.HttpResponseBadRequest()

        try:
            EmailAddressValidation.objects.create(address=email,
                                                  user_id=user_id)
        except IntegrityError:
            # 409 Conflict
            #   duplicated entries
            #   email exist and it's waiting for validation
            return http.HttpResponse(status=409)

        return http.HttpResponse(status=201)

    @method_decorator(login_required)
    def delete(self, request, key):
        """Remove an email address, validated or not."""

        request.DELETE = http.QueryDict(request.body)
        email_addr = request.DELETE.get('email')
        user_id = request.DELETE.get('user')

        if not email_addr:
            return http.HttpResponseBadRequest()

        try:
            email = EmailAddressValidation.objects.get(address=email_addr,
                                                       user_id=user_id)
        except EmailAddressValidation.DoesNotExist:
            pass
        else:
            email.delete()
            return http.HttpResponse(status=204)

        try:
            email = EmailAddress.objects.get(address=email_addr,
                                             user_id=user_id)
        except EmailAddress.DoesNotExist:
            raise http.Http404

        email.user = None
        email.save()
        return http.HttpResponse(status=204)

    @method_decorator(login_required)
    def update(self, request, key):
        """Set an email address as primary address."""

        request.UPDATE = http.QueryDict(request.body)

        email_addr = request.UPDATE.get('email')
        user_id = request.UPDATE.get('user')
        if not email_addr:
            return http.HttpResponseBadRequest()

        try:
            email = EmailAddress.objects.get(address=email_addr,
                                             user_id=user_id)
        except EmailAddress.DoesNotExist:
            raise http.Http404

        email.user.email = email_addr
        email.user.save()
        return http.HttpResponse(status=204)


class EmailValidationView(View):

    http_method_names = [u'post']

    def post(self, request):
        email_addr = request.POST.get('email')
        user_id = request.POST.get('user')
        try:
            email = EmailAddressValidation.objects.get(address=email_addr,
                                                       user_id=user_id)
        except EmailAddressValidation.DoesNotExist:
            raise http.Http404

        try:
            location = reverse('archive_email_view',
                               kwargs={'key': email.validation_key})
            verification_url = request.build_absolute_uri(location)
            send_verification_email(email_addr, email.user,
                                    email.validation_key, verification_url)
        except smtplib.SMTPException:
            logging.exception('Error sending validation email')
            return http.HttpResponseServerError()

        return http.HttpResponse(status=204)


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


class MailingListView(ListView):
    http_method_names = [u'get']
    template_name = 'mailinglist-summary.html'
    paginate_by = 6
    model = Thread

    def __init__(self, *args, **kwargs):
        super(MailingListView, self).__init__(*args, **kwargs)
        self.order_data = {
            'latest': {
                'name': _(u'Recent activity'),
                'field': '-latest_message__received_time'
            },
            'rating': {
                'name': _(u'Rating'),
                'field': '-score'
            }
        }

    def dispatch(self, request, *args, **kwargs):
        mailinglist = MailingList.objects.get(name=kwargs['mailinglist'])

        if mailinglist.is_private:
            if not request.user.is_authenticated():
                error_message = _("You are not logged in")
                messages.add_message(request, messages.ERROR, error_message)
                return redirect('login')

            if not self.check_list_membership(request.user, mailinglist.name):
                return redirect('user_list_subscriptions',
                                username=request.user)

        return super(MailingListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        mailinglist_name = self.kwargs['mailinglist']

        query = Q(mailinglist__name__iexact=mailinglist_name)

        order = self.request.GET.get('order', 'latest')
        order = self.order_data.get(order)

        result = Thread.objects.filter(query).order_by(order['field'])

        return result

    def get_context_data(self, **kwargs):
        context = super(MailingListView, self).get_context_data(**kwargs)
        mailinglist = MailingList.objects.get(name=self.kwargs['mailinglist'])

        context['mailinglist'] = mailinglist
        context['order_data'] = self.order_data
        context['selected'] = self.request.GET.get('order', 'latest')

        return context

    def check_list_membership(self, user, mailinglist_name):
        user = User.objects.get(username=user)
        lists_for_user = mailman.get_user_mailinglists(user)
        listnames_for_user = mailman.extract_listname_from_list(
            lists_for_user)

        if mailinglist_name not in listnames_for_user:
            error_message = _("You don't have permission to access this list")
            messages.add_message(self.request, messages.ERROR, error_message)

            return False

        return True
