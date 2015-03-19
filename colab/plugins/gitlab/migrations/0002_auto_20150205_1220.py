# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gitlab', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitlabComment',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Gitlab Comments',
                'verbose_name_plural': 'Gitlab Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GitlabIssue',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('state', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='gitlab.GitlabProject', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Gitlab Collaboration',
                'verbose_name_plural': 'Gitlab Collaborations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GitlabMergeRequest',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('target_branch', models.TextField()),
                ('source_branch', models.TextField()),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('state', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='gitlab.GitlabProject', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Gitlab Merge Request',
                'verbose_name_plural': 'Gitlab Merge Requests',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='gitlabproject',
            options={'verbose_name': 'Gitlab Project', 'verbose_name_plural': 'Gitlab Projects'},
        ),
    ]
