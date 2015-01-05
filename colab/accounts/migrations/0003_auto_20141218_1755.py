# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_needs_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='needs_update',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
