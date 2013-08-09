#!/usr/bin/env python
# encoding: utf-8

import uuid
from colab.deprecated import signup as signup_

from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404

from .forms import UserCreationForm
from super_archives.models import UserProfile, EmailAddress


def signup(request):

    # If the request method is GET just return the form
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'accounts/signup-form.html', {'form': form})

    # If the request method is POST try to store data
    form = UserCreationForm(request.POST)

    # If there is validation errors give the form back to the user
    if not form.is_valid():
        return render(request, 'accounts/signup-form.html', {'form': form})

    user = User(
        username=form.cleaned_data.get('username'),
        email=form.cleaned_data.get('email'),
        first_name=form.cleaned_data.get('first_name'),
        last_name=form.cleaned_data.get('last_name'),
        is_active=False,
    )
    user.set_password(form.cleaned_data.get('password1'))
    user.save()

    profile = UserProfile(
        user=user,
        institution=form.cleaned_data.get('institution'),
        role=form.cleaned_data.get('role'),
        twitter=form.cleaned_data.get('twitter'),
        facebook=form.cleaned_data.get('facebook'),
        google_talk=form.cleaned_data.get('google_talk'),
        webpage=form.cleaned_data.get('webpage'),
        verification_hash=uuid.uuid4().get_hex(),
    )
    profile.save()

    signup_.send_verification_email(request, user)

    mailing_lists = form.cleaned_data.get('lists')
    if mailing_lists:
        signup_.send_email_lists(user, mailing_lists)


    # Check if the user's email have been used previously
    #   in the mainling lists to link the user to old messages
    email_addr, created = EmailAddress.objects.get_or_create(address=user.email)
    if created:
        email_addr.real_name = user.get_full_name()

    email_addr.user = user
    email_addr.save()

    template_data = {
        'msg': _((u'Registration completed successfully. Please visit your '
                u'email address to validate it.')),
        'msg_css_class': 'success',
    }

    return render(request, 'accounts/account_message.html', template_data)


def verify_email(request, hash):
    """Verify hash and activate user's account"""

    profile = get_object_or_404(UserProfile, verification_hash=hash)

    profile.verification_hash = 'verified'
    profile.save()

    profile.user.is_active = True
    profile.user.save()

    template_data = {
        'msg': _(u'E-mail validated correctly.'),
        'msg_css_class': 'success',
    }

    return render(request, 'accounts/account_message.html', template_data)
