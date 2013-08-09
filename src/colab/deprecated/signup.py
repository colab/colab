#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail


def send_verification_email(request, user):
    
    subject = _(u'Colab: Checking e-mail')
    from_ = settings.SERVER_EMAIL
    to = user.email
    
    email_data = {
        'hash': user.profile.verification_hash,
        'server_name': request.get_host(),
    }

    html_content = render_to_string('accounts/email_signup-email-confirmation.html',
                                    email_data)
    text_content = strip_tags(html_content)
    email_msg = EmailMultiAlternatives(subject, text_content, from_, [to])
    email_msg.attach_alternative(html_content, 'text/html')
    email_msg.send()


def send_email_lists(user, mailing_lists):
    subject = _(u'Registration on the mailing list')
    from_ = user.email
    to = []
    for list_name in mailing_lists:
        # TODO: The following line needs to be generic. Domain should be stored in settings file
        #  or database (perharps read directly from mailman).
        subscribe_addr = list_name + '-subscribe@listas.interlegis.gov.br'
        to.append(subscribe_addr)

    send_mail(subject, '', from_, to)

