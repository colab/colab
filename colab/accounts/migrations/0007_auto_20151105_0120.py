# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import colab.accounts.utils.email


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20150828_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.EmailField(unique=True, max_length=75)),
                ('real_name', models.CharField(db_index=True, max_length=64, blank=True)),
                ('md5', models.CharField(max_length=32, null=True)),
                ('user', models.ForeignKey(related_name='emails', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailAddressValidation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.EmailField(unique=True, max_length=75)),
                ('validation_key', models.CharField(default=colab.accounts.utils.email.get_validation_key, max_length=32, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='emails_not_validated', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='emailaddressvalidation',
            unique_together=set([('user', 'address')]),
        ),
    ]
