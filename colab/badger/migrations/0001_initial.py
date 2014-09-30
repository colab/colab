# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, null=True, verbose_name='Title', blank=True)),
                ('description', models.CharField(max_length=200, null=True, verbose_name='Description', blank=True)),
                ('image_base64', models.TextField(verbose_name='Image')),
                ('type', models.CharField(max_length=200, verbose_name='Type', choices=[('auto', 'Automatically'), ('manual', 'Manual')])),
                ('user_attr', models.CharField(blank=True, max_length=100, null=True, verbose_name='User attribute', choices=[('messages', 'Messages'), ('contributions', 'Contributions'), ('wikis', 'Wikis'), ('revisions', 'Revisions'), ('tickets', 'Ticket')])),
                ('comparison', models.CharField(blank=True, max_length=10, null=True, verbose_name='Comparison', choices=[('gte', 'Greater than or equal'), ('lte', 'less than or equal'), ('equal', 'Equal'), ('biggest', 'Biggest')])),
                ('value', models.PositiveSmallIntegerField(null=True, verbose_name='Value', blank=True)),
                ('order', models.PositiveSmallIntegerField(default=100, verbose_name='Order')),
                ('awardees', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='Awardees', blank=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Badge',
                'verbose_name_plural': 'Badges',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BadgeI18N',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('i18n_language', models.CharField(max_length=10, verbose_name='language', choices=[(b'pt-br', 'Portuguese'), (b'es', 'Spanish')])),
                ('title', models.CharField(max_length=200, null=True, verbose_name='Title', blank=True)),
                ('description', models.CharField(max_length=200, null=True, verbose_name='Description', blank=True)),
                ('i18n_source', models.ForeignKey(related_name=b'translations', editable=False, to='badger.Badge', verbose_name='source')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='badgei18n',
            unique_together=set([('i18n_source', 'i18n_language')]),
        ),
    ]
