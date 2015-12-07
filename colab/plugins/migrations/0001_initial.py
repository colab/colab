# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeStampPlugin',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0), blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
