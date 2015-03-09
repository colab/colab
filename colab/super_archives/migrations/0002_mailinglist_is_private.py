# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('super_archives', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailinglist',
            name='is_private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
