# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitlab', '0003_auto_20150211_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitlabcomment',
            name='iid',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabmergerequest',
            name='iid',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
