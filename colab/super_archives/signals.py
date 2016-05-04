from .models import EmailAddress
from django.dispatch import receiver
from colab.accounts.signals import (delete_user)


@receiver(delete_user)
def delete_user_from_superarchive(sender, **kwargs):
    pass
    user = kwargs.get('user')
    emails = []

    if kwargs.get('emails'):
        emails = kwargs.get('emails').split(' ')

    for email in emails:
        EmailAddress.objects.filter(address=email).first().delete()
        user.update_subscription(email, [])
