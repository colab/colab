# -*- coding: utf-8 -*-
import datetime
from django.db import connections
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        # Selecting trac database
        connection = connections['trac']

        cursor = connection.cursor()
        cursor.execute('''
            CREATE OR REPLACE VIEW revision_view AS SELECT
                revision.rev,
                revision.author,
                revision.message,
                repository.value AS repository_name,
                TIMESTAMP WITH TIME ZONE 'epoch' + (revision.time/1000000) * INTERVAL '1s' AS created,
                CONCAT(revision.repos, '-', revision.rev) AS key
            FROM revision
            INNER JOIN repository ON(
                repository.id = revision.repos
                AND repository.name = 'name'
                AND repository.value != ''
            );
        ''')

    def backwards(self, orm):
        # Selecting trac database
        connection = connections['trac']

        cursor = connection.cursor()
        cursor.execute('''
            CREATE OR REPLACE VIEW revision_view AS SELECT
                revision.rev,
                revision.author,
                revision.message,
                repository.value AS repository_name,
                TIMESTAMP WITH TIME ZONE 'epoch' + (revision.time/1000000) * INTERVAL '1s' AS created
            FROM revision
            INNER JOIN repository ON(
                repository.id = revision.repos
                AND repository.name = 'name'
                AND repository.value != ''
            );
        ''')

    models = {
        u'proxy.revision': {
            'Meta': {'object_name': 'Revision', 'db_table': "'revision_view'", 'managed': 'False'},
            'author': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'repository_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rev': ('django.db.models.fields.TextField', [], {'primary_key': 'True'})
        },
        u'proxy.ticket': {
            'Meta': {'object_name': 'Ticket', 'db_table': "'ticket_view'", 'managed': 'False'},
            'author': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'collaborators': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'component': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'milestone': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reporter': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'severity': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'proxy.wiki': {
            'Meta': {'object_name': 'Wiki', 'db_table': "'wiki_view'", 'managed': 'False'},
            'author': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'collaborators': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'wiki_text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['proxy']
    symmetrical = True
