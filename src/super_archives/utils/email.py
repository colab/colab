
from django.core import mail
from django.conf import settings
from django.template import Context, loader
from django.utils.translation import ugettext as _


def colab_send_email(subject, message, to):
    from_email = settings.COLAB_FROM_ADDRESS
    return mail.send_mail(subject, message, from_email, [to])


def send_verification_email(to, user, validation_key):
    subject = _('Please verify your email ') + u'{}'.format(to)
    msg_tmpl = loader.get_template('superarchives/emails/email_verification.txt')
    message = msg_tmpl.render(Context({'to': to, 'user': user,
                                       'key': validation_key,
                                       'SITE_URL': settings.SITE_URL}))
    return colab_send_email(subject, message, to)


def send_email_lists(user, mailing_lists):
    """XXX: this should be done using API instead of emails"""

    subject = _(u'Registration on the mailing list')
    from_ = user.email
    to = []
    for list_name in mailing_lists:
        # TODO: The following line needs to be generic. Domain should be stored in settings file
        #  or database (perharps read directly from mailman).
        subscribe_addr = list_name + '-subscribe@listas.interlegis.gov.br'
        to.append(subscribe_addr)

    mail.send_mail(subject, '', from_, to)
