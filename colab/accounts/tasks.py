
from datetime import timedelta
from django.utils import timezone
from celery.decorators import periodic_task
from django.conf import settings

from .models import User

@periodic_task(run_every=timedelta(minutes=60))
def account_verification():
    limit = settings.ACCOUNT_VERIFICATION_TIME

    inactive_users = User.objects.filter(is_active=False)
    for user in inactive_users:
        delta_time = timezone.now() - user.modified
        if delta_time > limit:
            user.delete()
