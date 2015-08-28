# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import hitcounter.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GitlabComment',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('issue_comment', models.BooleanField(default=True)),
                ('parent_id', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Gitlab Comments',
                'verbose_name_plural': 'Gitlab Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GitlabGroup',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=100)),
                ('owner_id', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Gitlab Group',
                'verbose_name_plural': 'Gitlab Groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GitlabIssue',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('iid', models.IntegerField(null=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('state', models.TextField()),
                ('created_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Gitlab Issue',
                'verbose_name_plural': 'Gitlab Issues',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GitlabMergeRequest',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('iid', models.IntegerField(null=True)),
                ('target_branch', models.TextField()),
                ('source_branch', models.TextField()),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('state', models.TextField()),
                ('created_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Gitlab Merge Request',
                'verbose_name_plural': 'Gitlab Merge Requests',
            },
            bases=(models.Model,),
        ),
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
                ('path_with_namespace', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Gitlab Project',
                'verbose_name_plural': 'Gitlab Projects',
            },
            bases=(models.Model, hitcounter.models.HitCounterModelMixin),
        ),
        migrations.AddField(
            model_name='gitlabmergerequest',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='gitlab.GitlabProject', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabmergerequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabissue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='gitlab.GitlabProject', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabissue',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabcomment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='gitlab.GitlabProject', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gitlabcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
