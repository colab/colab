# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GitlabProject',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('description', models.TextField()),
                ('public', models.BooleanField(default=True)),
                ('name', models.TextField()),
                ('name_with_namespace', models.TextField()),
                ('created_at', models.DateTimeField(blank=True)),
                ('last_activity_at', models.DateTimeField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
