#!/usr/bin/env python
# encoding: utf-8

from collections import OrderedDict

from haystack.exceptions import SearchBackendError

from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, UpdateView, TemplateView

from conversejs import xmpp
from conversejs.models import XMPPAccount
from haystack.query import SearchQuerySet

from colab.super_archives.models import EmailAddress, Message, EmailAddressValidation
from colab.search.utils import trans
# from proxy.trac.models import WikiCollabCount, TicketCollabCount
from .forms import (UserCreationForm, UserCreationFormNoBrowserId, ListsForm, UserUpdateForm,
                    ChangeXMPPPasswordForm)
# from .errors import XMPPChangePwdException
from .utils import mailman


class LoginView(TemplateView):
    template_name = "accounts/login.html"


class UserProfileBaseMixin(object):
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user_'


class UserProfileUpdateView(UserProfileBaseMixin, UpdateView):
    template_name = 'accounts/user_update_form.html'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse('user_profile', kwargs={'username':
                                               self.object.username})

    def get_object(self, *args, **kwargs):
        obj = super(UserProfileUpdateView, self).get_object(*args, **kwargs)
        if self.request.user != obj and not self.request.user.is_superuser:
            raise PermissionDenied

        return obj

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        context['CONVERSEJS_ENABLED'] = getattr(settings, 'CONVERSEJS_ENABLED')
        return context


class UserProfileDetailView(UserProfileBaseMixin, DetailView):
    template_name = 'accounts/user_detail.html'

    def get_context_data(self, **kwargs):
        user = self.object
        context = {}

        count_types = OrderedDict()

        fields_or_lookup = (
            {'collaborators__contains': user.username},
            {'fullname_and_username__contains': user.username},
        )

        counter_class = {}
        # {
        #     'wiki': WikiCollabCount,
        #     'ticket': TicketCollabCount,
        # }

        types = ['thread']
        # types.extend(['ticket', 'wiki', 'changeset', 'attachment'])

        messages = Message.objects.filter(from_address__user__pk=user.pk)
        for type in types:
            CounterClass = counter_class.get(type)
            if CounterClass:
                try:
                    counter = CounterClass.objects.get(author=user.username)
                except CounterClass.DoesNotExist:
                    count_types[trans(type)] = 0
                else:
                    count_types[trans(type)] = counter.count
            elif type == 'thread':
                count_types[trans(type)] = messages.count()
            else:
                sqs = SearchQuerySet()
                for filter_or in fields_or_lookup:
                    sqs = sqs.filter_or(type=type, **filter_or)
                count_types[trans(type)] = sqs.count()

        context['type_count'] = count_types

        sqs = SearchQuerySet()
        for filter_or in fields_or_lookup:
            sqs = sqs.filter_or(**filter_or).exclude(type='thread')

        try:
            context['results'] = sqs.order_by('-modified', '-created')[:10]
        except SearchBackendError:
            context['results'] = sqs.order_by('-modified')[:10]

        email_pks = [addr.pk for addr in user.emails.iterator()]
        query = Message.objects.filter(from_address__in=email_pks)
        query = query.order_by('-received_time')
        context['emails'] = query[:10]

        count_by = 'thread__mailinglist__name'
        context['list_activity'] = dict(messages.values_list(count_by)
                                                .annotate(Count(count_by))
                                                .order_by(count_by))

        context.update(kwargs)
        return super(UserProfileDetailView, self).get_context_data(**context)


def signup(request):
    BROWSERID_ENABLED = getattr(settings, 'BROWSERID_ENABLED', False)

    if BROWSERID_ENABLED:
        # If the user is not authenticated, redirect to login
        if not request.user.is_authenticated():
            return redirect('login')

    if request.user.is_authenticated():
        # If the user doesn't need to update its main data,
        #   redirect to its profile
        # It happens when user is created by browserid
        # and didn't set his/her main data
        if not request.user.needs_update:
            return redirect('user_profile', username=request.user.username)

    # If the user is authenticated in Persona, but not in the Colab then he
    # will be redirected to the register form.
    if request.method == 'GET':
        if BROWSERID_ENABLED:
            user_form = UserCreationForm()
        else:
            user_form = UserCreationFormNoBrowserId()
        lists_form = ListsForm()

        return render(request, 'accounts/user_create_form.html',
                      {'user_form': user_form, 'lists_form': lists_form})

    if BROWSERID_ENABLED:
        user_form = UserCreationForm(request.POST, instance=request.user)
    else:
        user_form = UserCreationFormNoBrowserId(request.POST)
    lists_form = ListsForm(request.POST)

    if not user_form.is_valid() or not lists_form.is_valid():
        return render(request, 'accounts/user_create_form.html',
                      {'user_form': user_form, 'lists_form': lists_form})

    user = user_form.save(commit=False)
    user.needs_update = False

    if not BROWSERID_ENABLED:
        user.is_active = False
        user.save()
        EmailAddressValidation.create(user.email, user)
    else:
        user.save()

    # Check if the user's email have been used previously
    #   in the mainling lists to link the user to old messages
    email_addr, created = EmailAddress.objects.get_or_create(
        address=user.email)
    if created:
        email_addr.real_name = user.get_full_name()

    email_addr.user = user
    email_addr.save()

    mailing_lists = lists_form.cleaned_data.get('lists')
    mailman.update_subscription(user.email, mailing_lists)

    messages.success(request, _('Your profile has been created!'))


    return redirect('user_profile', username=user.username)


class ManageUserSubscriptionsView(UserProfileBaseMixin, DetailView):
    http_method_names = [u'get', u'post']
    template_name = u'accounts/manage_subscriptions.html'

    def get_object(self, *args, **kwargs):
        obj = super(ManageUserSubscriptionsView, self).get_object(*args,
                                                                  **kwargs)
        if self.request.user != obj and not self.request.user.is_superuser:
            raise PermissionDenied

        return obj

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        for email in user.emails.values_list('address', flat=True):
            lists = self.request.POST.getlist(email)
            user.update_subscription(email, lists)

        return redirect('user_profile', username=user.username)

    def get_context_data(self, **kwargs):
        context = {}
        context['membership'] = {}

        user = self.get_object()
        emails = user.emails.values_list('address', flat=True)
        all_lists = mailman.all_lists(description=True)

        for email in emails:
            lists = []
            lists_for_address = mailman.address_lists(email)
            for listname, description in all_lists:
                if listname in lists_for_address:
                    checked = True
                else:
                    checked = False
                lists.append((
                    {'listname': listname, 'description': description},
                    checked
                ))

            context['membership'].update({email: lists})

        context.update(kwargs)

        return super(ManageUserSubscriptionsView,
                     self).get_context_data(**context)


class ChangeXMPPPasswordView(UpdateView):
    model = XMPPAccount
    form_class = ChangeXMPPPasswordForm
    fields = ['password', ]
    template_name = 'accounts/change_password.html'

    def get_success_url(self):
        return reverse('user_profile', kwargs={
            'username': self.request.user.username
        })

    def get_object(self, queryset=None):
        obj = get_object_or_404(XMPPAccount, user=self.request.user.pk)
        self.old_password = obj.password
        return obj

    def form_valid(self, form):
        transaction.set_autocommit(False)

        response = super(ChangeXMPPPasswordView, self).form_valid(form)

        changed = xmpp.change_password(
            self.object.jid,
            self.old_password,
            form.cleaned_data['password1']
        )

        if not changed:
            messages.error(
                self.request,
                _(u'Could not change your password. Please, try again later.')
            )
            transaction.rollback()
            return response
        else:
            transaction.commit()

        messages.success(
            self.request,
            _("You've changed your password successfully!")
        )
        return response

def password_changed(request):
    #FIXME: This message was not translated yet.
    messages.success(request, _('Your password was changed.'))

    user = request.user

    return redirect('user_profile_update', username=user.username)

def password_reset_done_custom(request):
    messages.success(request, _('We\'ve emailed you instructions for setting your password. You should be receiving them shortly.'))

    return redirect('home')

def password_reset_complete_custom(request):
    #FIXME: This message was not translated yet.
    messages.success(request, _('Your password has been set. You may go ahead and log in now.'))

    return redirect('home')


