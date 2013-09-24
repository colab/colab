# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.institution'
        db.add_column(u'accounts_user', 'institution',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True),
                      keep_default=False)

        # Adding field 'User.role'
        db.add_column(u'accounts_user', 'role',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True),
                      keep_default=False)

        # Adding field 'User.twitter'
        db.add_column(u'accounts_user', 'twitter',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True),
                      keep_default=False)

        # Adding field 'User.facebook'
        db.add_column(u'accounts_user', 'facebook',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True),
                      keep_default=False)

        # Adding field 'User.google_talk'
        db.add_column(u'accounts_user', 'google_talk',
                      self.gf('django.db.models.fields.EmailField')(max_length=75, null=True),
                      keep_default=False)

        # Adding field 'User.webpage'
        db.add_column(u'accounts_user', 'webpage',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True),
                      keep_default=False)

        # Adding field 'User.verification_hash'
        db.add_column(u'accounts_user', 'verification_hash',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True),
                      keep_default=False)

        # Adding unique constraint on 'User', fields ['email']
        db.create_unique(u'accounts_user', ['email'])


    def backwards(self, orm):
        # Removing unique constraint on 'User', fields ['email']
        db.delete_unique(u'accounts_user', ['email'])

        # Deleting field 'User.institution'
        db.delete_column(u'accounts_user', 'institution')

        # Deleting field 'User.role'
        db.delete_column(u'accounts_user', 'role')

        # Deleting field 'User.twitter'
        db.delete_column(u'accounts_user', 'twitter')

        # Deleting field 'User.facebook'
        db.delete_column(u'accounts_user', 'facebook')

        # Deleting field 'User.google_talk'
        db.delete_column(u'accounts_user', 'google_talk')

        # Deleting field 'User.webpage'
        db.delete_column(u'accounts_user', 'webpage')

        # Deleting field 'User.verification_hash'
        db.delete_column(u'accounts_user', 'verification_hash')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'google_talk': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'verification_hash': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'webpage': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']