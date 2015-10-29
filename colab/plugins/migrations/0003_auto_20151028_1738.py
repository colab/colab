# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0002_auto_20151028_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timestampplugin',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0), blank=True),
            preserve_default=True,
        ),
    ]
