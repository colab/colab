
from uuid import uuid4

from django.core import mail
from django.conf import settings
from django.template import Context, loader
from django.utils.translation import ugettext as _

def get_validation_key():
    return uuid4().hex

def colab_send_email(subject, message, to):
    from_email = settings.COLAB_FROM_ADDRESS
    return mail.send_mail(subject, message, from_email, [to])


def send_verification_email(to, user, validation_key):
    subject = _('Please verify your email ') + u'{}'.format(to)
    msg_tmpl = \
        loader.get_template('accounts/emails/email_verification.txt')
    message = msg_tmpl.render(Context({'to': to, 'user': user,
                                       'key': validation_key,
                                       'SITE_URL': settings.SITE_URL}))
    return colab_send_email(subject, message, to)
