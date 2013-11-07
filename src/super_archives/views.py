# -*- coding: utf-8 -*-

import smtplib
import logging
import urlparse

import requests

from django import http
from django.conf import settings
from django.contrib import messages
from django.db import IntegrityError
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from haystack.query import SearchQuerySet

from .utils.email import send_verification_email
from .models import MailingList, Thread, EmailAddress, \
                    EmailAddressValidation, Message


class ThreadView(View):
    http_method_names = [u'get', u'post']

    def get(self, request, mailinglist, thread_token):

        thread = Thread.objects.get(subject_token=thread_token,
                                    mailinglist__name=mailinglist)
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

        data = {}
        data['from']  = '{} <{}>'.format(request.user.get_full_name(),
                                      request.user.email)
        data['subject'] = thread.message_set.first().subject_clean
        data['body'] = request.POST.get('emailbody', '').strip()

        url = urlparse.urljoin(settings.MAILMAN_API_URL, mailinglist + '/sendmail')

        error_msg = None
        try:
            resp = requests.post(url, data=data, timeout=2)
        except requests.exceptions.ConnectionError:
            resp = None
            error_msg = _('Error trying to connect to Mailman API')
        except requests.exceptions.Timeout:
            resp = None
            error_msg = _('Timout trying to connect to Mailman API')

        if resp and resp.status_code == 200:
            messages.success(request, _("Your message was sent. It may take "
                                        "some minutes before it's delivered. "
                                        "Why don't you breath some fresh air "
                                        "in the meanwhile."))
        else:
            if not error_msg:
                if resp is not None:
                    if resp.status_code == 400:
                        error_msg = _('You cannot send an empty email')
                    elif resp.status_code == 404:
                        error_msg = _('Mailing list does not exist')
                else:
                    error_msg = _('Unkown error trying to connect to Mailman API')
            messages.error(request, error_msg)

        return self.get(request, mailinglist, thread_token)


class ThreadDashboardView(View):
    http_method_names = ['get']

    def get(self, request):
        MAX = 6
        context = {}

        context['lists'] = []
        lists = MailingList.objects.filter()
        for list_ in MailingList.objects.order_by('name'):
            context['lists'].append((
                list_.name,
                list_.thread_set.filter(spam=False)[:MAX],
                SearchQuerySet().filter(type='thread', tag=list_.name)[:MAX],
            ))

        return render(request, 'superarchives/thread-dashboard.html', context)


class EmailView(View):

    http_method_names = [u'head', u'get', u'post', u'delete', u'update']

    def get(self, request, key):
        """Validate an email with the given key"""

        try:
            email_val = EmailAddressValidation.objects.get(validation_key=key,
                                                           user__pk=request.user.pk)
        except EmailAddressValidation.DoesNotExist:
            messages.error(request, _('The email address you are trying to '
                                      'verify either has already been verified '
                                      'or does not exist.'))
            return redirect('/')

        try:
            email = EmailAddress.objects.get(address=email_val.address)
        except EmailAddress.DoesNotExist:
            email = EmailAddress(address=email_val.address)

        if email.user:
            messages.error(request, _('The email address you are trying to '
                                      'verify is already an active email '
                                      'address.'))
            email_val.delete()
            return redirect('/')

        email.user = email_val.user
        email.save()
        email_val.delete()

        messages.success(request, _('Email address verified!'))
        return redirect('user_profile', username=email_val.user.username)


    @method_decorator(login_required)
    def post(self, request, key):
        """Create new email address that will wait for validation"""

        email = request.POST.get('email')
        if not email:
            return http.HttpResponseBadRequest()

        try:
            EmailAddressValidation.objects.create(address=email,
                                                  user=request.user)
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

        if not email_addr:
            return http.HttpResponseBadRequest()

        try:
            email = EmailAddressValidation.objects.get(address=email_addr,
                                                       user=request.user)
        except EmailAddressValidation.DoesNotExist:
            pass
        else:
            email.delete()
            return http.HttpResponse(status=204)

        try:
            email = EmailAddress.objects.get(address=email_addr,
                                             user=request.user)
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
        if not email_addr:
            return http.HttpResponseBadRequest()

        try:
            email = EmailAddress.objects.get(address=email_addr,
                                             user=request.user)
        except EmailAddress.DoesNotExist:
            raise http.Http404

        request.user.email = email_addr
        request.user.save()
        return http.HttpResponse(status=204)


class EmailValidationView(View):

    http_method_names = [u'post']

    def post(self, request):
        email_addr = request.POST.get('email')
        try:
            email = EmailAddressValidation.objects.get(address=email_addr,
                                                       user=request.user)
        except http.DoesNotExist:
            raise http.Http404

        try:
            send_verification_email(email_addr, request.user,
                                    email.validation_key)
        except smtplib.SMTPException:
            logging.exception('Error sending validation email')
            return http.HttpResponseServerError()

        return http.HttpResponse(status=204)
