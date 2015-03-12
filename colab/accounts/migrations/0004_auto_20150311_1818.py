# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def trim_fields(apps, schema_editor):
    trim_extra_account(apps, schema_editor, "facebook")
    trim_extra_account(apps, schema_editor, "github")
    trim_extra_account(apps, schema_editor, "twitter")

def trim_extra_account(apps, schema_editor, types):
    Users = apps.get_model('accounts', 'User')
    for user in Users.objects.all():
        field = getattr(user, types)
        if not field:
            continue
        tmpString = field.split("/")[-1]
        if len(field) >= 15:
            setattr(user, types, tmpString[:14])
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20141218_1755'),
    ]

    operations = [
        migrations.RunPython(trim_fields),
        migrations.AlterField(
            model_name='user',
            name='facebook',
            field=models.CharField(max_length=15, null=True, blank=True),
            preserve_default=True,
        ),

        migrations.AlterField(
            model_name='user',
            name='github',
            field=models.CharField(max_length=39, null=True, verbose_name='github', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter',
            field=models.CharField(max_length=15, null=True, blank=True),
            preserve_default=True,
        ),
    ]
