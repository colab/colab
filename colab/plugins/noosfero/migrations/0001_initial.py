# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NoosferoArticle',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.TextField()),
                ('path', models.TextField(null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('profile_identifier', models.TextField()),
                ('created_at', models.DateTimeField(blank=True)),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoosferoCategory',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoosferoCommunity',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('identifier', models.TextField()),
                ('description', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(blank=True)),
                ('categories', models.ManyToManyField(to='noosfero.NoosferoCategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Community',
                'verbose_name_plural': 'Communities',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='noosferoarticle',
            name='categories',
            field=models.ManyToManyField(to='noosfero.NoosferoCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noosferoarticle',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
