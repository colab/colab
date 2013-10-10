

from django.db.models import F
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core.management.base import BaseCommand, CommandError


from ...models import User


class Command(BaseCommand):
    """Delete user accounts that have never logged in.

    Delete from database user accounts that have never logged in
    and are at least 24h older.

    """

    help = __doc__

    def handle(self, *args, **kwargs):
        seconds = timezone.timedelta(seconds=1)
        now = timezone.now()
        one_day_ago = timezone.timedelta(days=1)

        # Query for users that have NEVER logged in
        #
        # By default django sets the last_login as auto_now and then
        #   last_login is pretty much the same than date_joined
        #   (instead of null as I expected). Because of that we query
        #   for users which last_login is between date_joined - N and
        #   date_joined + N, where N is a small constant in seconds.
        users = User.objects.filter(last_login__gt=(F('date_joined') - seconds),
                                    last_login__lt=(F('date_joined') + seconds),
                                    date_joined__lt=now-one_day_ago)
        count = 0
        for user in users:
            count += 1
            user.delete()

        print _(u'%(count)s users deleted.') % {'count': count}
