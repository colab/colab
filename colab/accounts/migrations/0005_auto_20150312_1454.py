# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from django.db import models, migrations
from django.utils.crypto import get_random_string


def normalize_password(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    for user in User.objects.all():
        if len(user.password) is not 0:
            continue

        rand_pwd = get_random_string()

        user.password = make_password(rand_pwd)
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150311_1818'),
    ]

    operations = [
        migrations.RunPython(normalize_password)
    ]
