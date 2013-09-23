#!/usr/bin/env python
# encoding: utf-8
"""
userprofile.py

Created by Sergio Campos on 2012-01-10.
"""

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from colab.deprecated import solrutils
from accounts.forms import UserCreationForm, UserUpdateForm
from super_archives.models import Message, UserProfile, EmailAddress



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
