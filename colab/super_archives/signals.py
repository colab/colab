
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import EmailAddress


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_email_address(sender, instance, created, **kwargs):
    if not created:
        return

    email, email_created = EmailAddress.objects.get_or_create(
        address=instance.email,
        defaults={
            'real_name': instance.get_full_name(),
            'user': instance,
        }
    )

    email.user = instance
    email.save()
