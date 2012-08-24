#!/usr/bin/env python
# encoding: utf-8
"""
signup.py

Created by Sergio Campos on 2012-01-10.
"""

import uuid
from colab import signup as signup_

from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.shortcuts import render_to_response, redirect, get_object_or_404

from colab.super_archives.forms import UserCreationForm
from colab.super_archives.models import UserProfile, EmailAddress


def signup(request):

    # If the request method is GET just return the form
    if request.method == 'GET':
        form = UserCreationForm()
        return render_to_response('signup-form.html', {'form': form}, 
                                  RequestContext(request))

    # If the request method is POST try to store data
    form = UserCreationForm(request.POST)
    
    # If there is validation errors give the form back to the user
    if not form.is_valid():
        return render_to_response('signup-form.html', {'form': form}, 
                                  RequestContext(request))

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
    
    return render_to_response('account_message.html', template_data,
                              RequestContext(request))


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
    
    return render_to_response('account_message.html', template_data,
                              RequestContext(request))
    

def request_reset_password(request):
    """Request a password reset.
    
    In case request method is GET it will display the password reset
    form. Otherwise we'll look for a username in the POST request to
    have its password reset. This user will receive a link where he
    will be allowed to change his password.
    
    """
    
    if request.method == 'GET':
        return render_to_response('account_request_reset_password.html', {},
                                  RequestContext(request))
    
    username = request.POST.get('username')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    
    if user and user.is_active:
        profile = user.profile
        profile.verification_hash = uuid.uuid4().get_hex()
        profile.save()
                
        signup_.send_reset_password_email(request, user)
    
    msg = _((u'For your safety, in a few moments you will receive '
           u'an email asking you to confirm the password '
           u'change request. Please wait.'))
    
    template_data = {
        'msg': msg,
        'msg_css_class': 'info', 
    }
    
    return render_to_response('account_message.html', template_data,
                              RequestContext(request))


def reset_password(request, hash):
    """Perform a password change.
    
    If the request method is set to GET and the hash matches a form 
    will be displayed to the user allowing the password change.
    If the request method is POST the user password will be changed
    to the newly set data.
    
    """
    
    profile = get_object_or_404(UserProfile, verification_hash=hash)
    user = profile.user
    
    form = SetPasswordForm(profile.user)
    
    template_data = {
        'form': form,
        'hash': hash,
    }
    
    if request.method == 'GET':
        return render_to_response('account_change_password.html', 
                                  template_data, RequestContext(request))


    form = SetPasswordForm(user, request.POST)
    template_data.update({'form': form})
    
    if not form.is_valid():
        return render_to_response('account_change_password.html', 
                                  template_data, RequestContext(request))

    profile.verification_hash = 'verified'
    profile.save()

    user.set_password(form.cleaned_data.get('new_password1'))
    user.save()

    template_data.update({
        'msg': _(u'Password changed successfully!'),
        'msg_css_class': 'success',
    })
    return render_to_response('account_message.html', template_data,
                              RequestContext(request))

@login_required
def change_password(request):
    """Change a password for an authenticated user."""
    
    form = PasswordChangeForm(request.user)
    
    template_data = {
        'form': form
    }
    
    if request.method == 'GET':
        return render_to_response('account_change_password.html',
                                  template_data, RequestContext(request))
    
    form = PasswordChangeForm(request.user, request.POST)
    template_data.update({'form': form})
    
    if not form.is_valid():
        return render_to_response('account_change_password.html', 
                                  template_data, RequestContext(request))
                                  
    request.user.set_password(form.cleaned_data.get('new_password1'))
    request.user.save()
    
    template_data.update({
        'msg': _(u'Password changed successfully!'),
        'msg_css_class': 'success',
    })
    return render_to_response('account_message.html', template_data,
                              RequestContext(request))    
    
