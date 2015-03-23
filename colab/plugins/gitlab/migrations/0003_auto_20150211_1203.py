# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gitlab', '0002_auto_20150205_1220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gitlabissue',
            options={'verbose_name': 'Gitlab Issue', 'verbose_name_plural': 'Gitlab Issues'},
        ),
        migrations.AddField(
            model_name='gitlabcomment',
            name='issue_comment',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabcomment',
            name='parent_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabcomment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='gitlab.GitlabProject', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabissue',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabmergerequest',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabproject',
            name='path_with_namespace',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gitlabcomment',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
