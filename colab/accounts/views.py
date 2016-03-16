# encoding: utf-8
from collections import OrderedDict

from django.contrib import messages
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, UpdateView
from django.http import Http404

from colab.super_archives.models import (EmailAddress,
                                         EmailAddressValidation)
from colab.plugins.utils.collaborations import (get_collaboration_data,
                                                get_visible_threads)
from colab.accounts.models import User

from .forms import (ColabSetUsernameForm, ListsForm, UserUpdateForm)
from .utils import mailman


class UserProfileBaseMixin(object):
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user_'


class UserProfileUpdateView(UserProfileBaseMixin, UpdateView):
    template_name = 'accounts/user_update_form.html'
    form_class = UserUpdateForm

    def post(self, request, *args, **kwargs):
        if not request.POST.get('colab_form'):
            request.method = 'GET'
            result = super(UserProfileUpdateView, self).get(request, *args,
                                                            **kwargs)
        else:
            result = super(UserProfileUpdateView, self).post(request, *args,
                                                             **kwargs)
        return result

    def get_success_url(self):
        return reverse('user_profile', kwargs={'username':
                                               self.object.username})

    def get_object(self, *args, **kwargs):
        obj = super(UserProfileUpdateView, self).get_object(*args, **kwargs)
        if self.request.user != obj and not self.request.user.is_superuser:
            raise PermissionDenied

        return obj


class UserProfileDetailView(UserProfileBaseMixin, DetailView):
    template_name = 'accounts/user_detail.html'

    def get_context_data(self, **kwargs):
        profile_user = self.object
        context = {}

        count_types = OrderedDict()

        logged_user = None
        if self.request.user.is_authenticated():
            logged_user = User.objects.get(username=self.request.user)

        collaborations, count_types_extras = get_collaboration_data(
            logged_user, profile_user)

        collaborations.sort(key=lambda elem: elem.modified, reverse=True)

        count_types.update(count_types_extras)

        context['type_count'] = count_types
        context['results'] = collaborations[:10]

        query = get_visible_threads(logged_user, profile_user)
        context['emails'] = query.order_by('-received_time')[:10]

        count_by = 'thread__mailinglist__name'
        context['list_activity'] = dict(query.values_list(count_by)
                                        .annotate(Count(count_by))
                                        .order_by(count_by))

        context.update(kwargs)
        return super(UserProfileDetailView, self).get_context_data(**context)


def signup(request):

    if request.user.is_authenticated():
        if not request.user.needs_update:
            return redirect('user_profile', username=request.user.username)

    if request.method == 'GET':
        user_form = ColabSetUsernameForm()
        lists_form = ListsForm()

        return render(request, 'accounts/user_create_form.html',
                      {'user_form': user_form, 'lists_form': lists_form})

    user_form = ColabSetUsernameForm(request.POST)
    lists_form = ListsForm(request.POST)

    if not user_form.is_valid() or not lists_form.is_valid():
        return render(request, 'accounts/user_create_form.html',
                      {'user_form': user_form, 'lists_form': lists_form})

    user = user_form.save(commit=False)
    user.needs_update = False

    user.is_active = False
    user.save()
    email = EmailAddressValidation.create(user.email, user)

    location = reverse('archive_email_view',
                       kwargs={'key': email.validation_key})
    verification_url = request.build_absolute_uri(location)
    EmailAddressValidation.verify_email(email, verification_url)

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
            info_messages = user.update_subscription(email, lists)
            for msg_type, message in info_messages:
                show_message = getattr(messages, msg_type)
                show_message(request, _(message))

        return redirect('user_profile', username=user.username)

    def get_context_data(self, **kwargs):
        context = {}
        context['membership'] = {}

        user = self.get_object()
        emails = user.emails.values_list('address', flat=True)
        all_lists = mailman.all_lists()

        for email in emails:
            lists = []
            lists_for_address = mailman.mailing_lists(address=email,
                                                      names_only=True)
            for mlist in all_lists:
                if mlist.get('listname') in lists_for_address:
                    checked = True
                else:
                    checked = False
                lists.append((
                    {'listname': mlist.get('listname'),
                     'description': mlist.get('description')},
                    checked
                ))

            context['membership'].update({email: lists})

        context.update(kwargs)

        return super(ManageUserSubscriptionsView,
                     self).get_context_data(**context)


def password_changed(request):
    messages.success(request, _('Your password was changed.'))

    user = request.user

    return redirect('user_profile_update', username=user.username)


def password_reset_done_custom(request):
    msg = _(("We've emailed you instructions for setting "
             "your password. You should be receiving them shortly."))
    messages.success(request, msg)

    return redirect('home')


def password_reset_complete_custom(request):
    msg = _('Your password has been set. You may go ahead and log in now.')
    messages.success(request, msg)

    return redirect('home')


def myaccount_redirect(request, route):
    if not request.user.is_authenticated():
        raise Http404()

    url = '/'.join(('/account', request.user.username, route))

    return redirect(url)
