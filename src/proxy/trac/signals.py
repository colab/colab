
from django.db import connections
from django.dispatch import receiver
from django.db.models.signals import post_save

from accounts.models import User


@receiver(post_save, sender=User)
def change_session_attribute_email(sender, instance, **kwargs):
    cursor = connections['trac'].cursor()

    cursor.execute(("UPDATE session_attribute SET value=%s "
                    "WHERE name='email' AND sid=%s"),
                    [instance.email, instance.username])
    cursor.execute(("UPDATE session_attribute SET value=%s "
                    "WHERE name='name' AND sid=%s"),
                    [instance.get_full_name(), instance.username])

    cursor.execute(("INSERT INTO session_attribute "
                    "(sid, authenticated,  name, value) "
                    "SELECT %s, '1', 'email', %s WHERE NOT EXISTS "
                    "(SELECT 1 FROM session_attribute WHERE sid=%s "
                    "AND name='email')"),
                    [instance.username, instance.email, instance.username])

    cursor.execute(("INSERT INTO session_attribute "
                    "(sid, authenticated, name, value) "
                    "SELECT %s, '1', 'name', %s WHERE NOT EXISTS "
                    "(SELECT 1 FROM session_attribute WHERE sid=%s "
                    "AND name='name')"),
                    [instance.username, instance.get_full_name(),
                     instance.username])
