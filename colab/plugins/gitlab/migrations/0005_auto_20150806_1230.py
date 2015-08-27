# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitlab', '0004_auto_20150630_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gitlabcomment',
            name='iid',
        ),
        migrations.AddField(
            model_name='gitlabissue',
            name='iid',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
