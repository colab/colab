from datetime import timedelta

from celery.decorators import periodic_task
from colab.accounts.models import User
from django.conf import settings
from django.utils import timezone


@periodic_task(run_every=timedelta(minutes=60))
def account_verification():
    limit = settings.ACCOUNT_VERIFICATION_TIME

    inactive_users = User.objects.filter(is_active=False)
    for user in inactive_users:
        delta_time = timezone.now() - user.modified
        if delta_time > limit:
            user.delete()
