# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hitcounter.models
import taggit.managers
import django.db.models.deletion
from django.conf import settings
import colab.super_archives.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('address', models.EmailField(unique=True, max_length=75)),
                ('real_name', models.CharField(db_index=True, max_length=64,
                                               blank=True)),
                ('md5', models.CharField(max_length=32, null=True)),
                ('user', models.ForeignKey(related_name=b'emails',
                 on_delete=django.db.models.deletion.SET_NULL,
                 to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailAddressValidation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('address', models.EmailField(unique=True, max_length=75)),
                ('validation_key',
                 models.CharField(
                     default=colab.super_archives.models.get_validation_key,
                     max_length=32, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user',
                 models.ForeignKey(related_name=b'emails_not_validated',
                                   to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=b'128')),
                ('weight', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('?',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=75)),
                ('description', models.TextField()),
                ('logo', models.FileField(upload_to=b'list_logo')),
                ('last_imported_index', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailingListMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('mailinglist',
                 models.ForeignKey(to='super_archives.MailingList')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('subject',
                 models.CharField(help_text='Please enter a message subject',
                                  max_length=512, verbose_name='Subject',
                                  db_index=True)),
                ('subject_clean', models.CharField(max_length=512,
                                                   db_index=True)),
                ('body',
                 models.TextField(default=b'',
                                  help_text='Please enter a message body',
                                  verbose_name='Message body')),
                ('received_time', models.DateTimeField(db_index=True)),
                ('message_id', models.CharField(max_length=512)),
                ('spam', models.BooleanField(default=False)),
                ('from_address',
                 models.ForeignKey(to='super_archives.EmailAddress')),
            ],
            options={
                'ordering': ('received_time',),
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('is_reply', models.BooleanField(default=False)),
                ('order', models.IntegerField()),
                ('message', models.ForeignKey(related_name=b'blocks',
                                              to='super_archives.Message')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('value', models.TextField()),
                ('Message', models.ForeignKey(to='super_archives.Message')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('subject_token', models.CharField(max_length=512)),
                ('score', models.IntegerField(default=0,
                                              help_text='Thread score',
                                              verbose_name='Score')),
                ('spam', models.BooleanField(default=False)),
                ('latest_message',
                 models.OneToOneField(related_name=b'+',
                                      null=True, to='super_archives.Message',
                                      help_text='Latest message posted',
                                      verbose_name='Latest message')),
                ('mailinglist',
                 models.ForeignKey(
                     verbose_name='Mailing List',
                     to='super_archives.MailingList',
                     help_text='The Mailing List where is the thread')),
                ('tags',
                 taggit.managers.TaggableManager(
                     to='taggit.Tag',
                     through='taggit.TaggedItem',
                     help_text='A comma-separated list of tags.',
                     verbose_name='Tags')),
            ],
            options={
                'ordering': ('-latest_message__received_time',),
                'verbose_name': 'Thread',
                'verbose_name_plural': 'Threads',
            },
            bases=(models.Model, hitcounter.models.HitCounterModelMixin),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(to='super_archives.Message')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'message')]),
        ),
        migrations.AlterUniqueTogether(
            name='thread',
            unique_together=set([('subject_token', 'mailinglist')]),
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(to='super_archives.Thread', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='message',
            unique_together=set([('thread', 'message_id')]),
        ),
        migrations.AddField(
            model_name='keyword',
            name='thread',
            field=models.ForeignKey(to='super_archives.Thread'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='emailaddressvalidation',
            unique_together=set([('user', 'address')]),
        ),
    ]
