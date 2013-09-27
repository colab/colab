#!/usr/bin/env python
# encoding: utf-8

from django.contrib import messages

from django.contrib.auth import get_user_model
from django.views.generic import DetailView, UpdateView
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from colab.deprecated import solrutils
from colab.deprecated import signup as signup_

from super_archives.models import EmailAddress, Message
from .forms import UserCreationForm, ListsForm, UserUpdateForm


class UserProfileBaseMixin(object):
    model = get_user_model()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user_'


class UserProfileUpdateView(UserProfileBaseMixin, UpdateView):
    template_name = 'accounts/user_update_form.html'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse('user_profile', kwargs={'username': self.object.username})



class UserProfileDetailView(UserProfileBaseMixin, DetailView):
    template_name = 'accounts/user_detail.html'

    def get_context_data(self, **kwargs):
        user = self.object
        context = {}

        # TODO: Use haystack instead of solrutils
        context['type_count'] = solrutils.count_types(
            filters={'collaborator': user.username}
        )

        # TODO: Use haystack instead of solrutils
        context['docs'] = solrutils.get_latest_collaborations(
            username=user.username
        )

        email_pks = [addr.pk for addr in user.emails.iterator()]
        query = Message.objects.filter(from_address__in=email_pks)
        query = query.order_by('-received_time')
        context['emails'] = query[:10]

        context.update(kwargs)
        return super(UserProfileDetailView, self).get_context_data(**context)


def signup(request):
    # If the request method is GET just return the form
    if request.method == 'GET':
        user_form = UserCreationForm()
        lists_form = ListsForm()
        return render(request, 'accounts/user_create_form.html',
                      {'user_form': user_form, 'lists_form': lists_form})

    user_form = UserCreationForm(request.POST)
    lists_form = ListsForm(request.POST)

    if not user_form.is_valid() or not lists_form.is_valid():
        return render(request, 'accounts/user_create_form.html',
                      {'user_form': user_form, 'lists_form': lists_form})

    user = user_form.save()

    mailing_lists = lists_form.cleaned_data.get('lists')
    if mailing_lists:
        signup_.send_email_lists(user, mailing_lists)

    # Check if the user's email have been used previously
    #   in the mainling lists to link the user to old messages
    email_addr, created = EmailAddress.objects.get_or_create(address=user.email)
    if created:
        email_addr.real_name = user.get_full_name()

    email_addr.user = user
    email_addr.save()

    messages.success(request, _('Your profile has been created!'))
    messages.warning(request, _('You must login to validated your profile. '
                                'Profiles not validated are deleted in 24h.'))

    return redirect('user_profile', username=user.username)
