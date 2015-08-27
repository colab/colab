
from django.core import mail
from django.conf import settings
from django.template import Context, loader
from django.utils.translation import ugettext as _


def colab_send_email(subject, message, to):
    from_email = settings.COLAB_FROM_ADDRESS
    return mail.send_mail(subject, message, from_email, [to])


def send_verification_email(to, user, validation_key, verification_url):
    subject = _('Please verify your email ') + u'{}'.format(to)
    msg_tmpl = \
        loader.get_template('superarchives/emails/email_verification.txt')
    message = msg_tmpl.render(Context({'to': to, 'user': user,
                                       'verification_url': verification_url
                                       }))
    return colab_send_email(subject, message, to)
