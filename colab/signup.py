#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_verification_email(request, user):
    
    subject = _(u'Colab: Verificação de email')
    from_ = settings.SERVER_EMAIL
    to = user.email
    
    email_data = {
        'hash': user.profile.verification_hash,
        'server_name': request.get_host(),
    }

    html_content = render_to_string('email_signup-email-confirmation.html', 
                                     email_data)
    text_content = strip_tags(html_content)
    email_msg = EmailMultiAlternatives(subject, text_content, from_, [to])
    email_msg.attach_alternative(html_content, 'text/html')
    email_msg.send()


def send_reset_password_email(request, user):

    subject = _(u'Altereção de senha do Colab Interlegis')
    from_ = settings.SERVER_EMAIL
    to = user.email
    
    email_data = {
        'hash': user.profile.verification_hash,
        'server_name': request.get_host(),
        'username': user.username,
    }
    
    html_content = render_to_string('email_account-reset-password.html', 
                                    email_data)
    text_content = strip_tags(html_content)
    
    email_msg = EmailMultiAlternatives(subject, text_content, from_, [to])
    email_msg.attach_alternative(html_content, 'text/html')
    email_msg.send()
    
    