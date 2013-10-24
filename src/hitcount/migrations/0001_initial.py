# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hit'
        db.create_table(u'hitcount_hit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(auto_now=True, db_index=True, blank=True)),
            ('hits', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'hitcount', ['Hit'])

        # Adding unique constraint on 'Hit', fields ['content_type', 'object_pk']
        db.create_unique(u'hitcount_hit', ['content_type_id', 'object_pk'])


    def backwards(self, orm):
        # Removing unique constraint on 'Hit', fields ['content_type', 'object_pk']
        db.delete_unique(u'hitcount_hit', ['content_type_id', 'object_pk'])

        # Deleting model 'Hit'
        db.delete_table(u'hitcount_hit')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hitcount.hit': {
            'Meta': {'unique_together': "(('content_type', 'object_pk'),)", 'object_name': 'Hit'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'hits': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['hitcount']