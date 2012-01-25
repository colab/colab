#!/usr/bin/env python
# encoding: utf-8
"""
userprofile.py

Created by Sergio Campos on 2012-01-10.
"""

from django.template import RequestContext
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect

from colab import solrutils
from colab.super_archives.forms import UserCreationForm, UserUpdateForm
from colab.super_archives.models import Message, UserProfile, EmailAddress
                                        

def read(request, user, email_address=None, editable=False, form=None):
    
    if form is None:
        form = UserCreationForm()
    
    if user:
        email_addresses = user.emails.all()
        profile = user.profile
        last_modified_docs = solrutils.get_latest_collaborations(
            username=user.username
        )
        
        type_count = solrutils.count_types(
            filters={'collaborator': user.username}
        )
        
    else:
        email_addresses = [email_address]
        profile = None
        last_modified_docs = []
        type_count = {}
        
    if not email_address and email_addresses:
        email_address = email_addresses[0]

    email_addresses_ids = tuple([str(addr.id) for addr in email_addresses])
    
    query = """
    SELECT 
        * 
    FROM
        super_archives_message JOIN (
            SELECT id
            FROM super_archives_message
            WHERE from_address_id IN (%(ids)s)
            GROUP BY thread_id, id
        ) AS subquery 
        ON subquery.id = super_archives_message.id
    ORDER BY 
        received_time DESC
    LIMIT 10;
    
    """ % {'ids': ','.join(email_addresses_ids)}

    emails = Message.objects.raw(query)
    #n_sent = Message.objects.filter(from_address__in=email_addresses).count()

    template_data = {
        'user_profile': profile,
        'email_address': email_address,
        'emails': emails or [],
        'form': form,
        'editable': editable,
        'type_count': type_count,
        'docs': last_modified_docs,
    }
    
    return render_to_response('user-profile.html', template_data, 
                              RequestContext(request))


@login_required
def by_request_user(request):
    return read(request, request.user)


def by_username(request, username):
    user = get_object_or_404(User, username=username)
    return read(request, user)


def by_emailhash(request, emailhash):
    email_addr = get_object_or_404(EmailAddress, md5=emailhash)
    return read(request, email_addr.user, email_addr)


@login_required
def update(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)
    form = UserUpdateForm(initial=model_to_dict(profile))
    
    if request.method == "GET":
        return read(request, profile.user, editable=True, form=form)

    form = UserUpdateForm(request.POST)
    if not form.is_valid():
        return read(request, profile.user, editable=True, form=form)

    profile.institution = form.cleaned_data.get('institution')
    profile.role = form.cleaned_data.get('role')
    profile.twitter = form.cleaned_data.get('twitter')
    profile.facebook = form.cleaned_data.get('facebook')
    profile.google_talk = form.cleaned_data.get('google_talk')
    profile.webpage = form.cleaned_data.get('webpage')
    profile.save()
    
    return redirect('user_profile', profile.user.username)
