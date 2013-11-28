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
            CREATE OR REPLACE VIEW wiki_view AS SELECT
                wiki.name AS name,
                (SELECT wiki2.text FROM wiki AS wiki2 WHERE wiki2.name = wiki.name
                 AND wiki2.version = MAX(wiki.version)) AS wiki_text,
                (SELECT wiki3.author FROM wiki AS wiki3 WHERE wiki3.name = wiki.name
                 AND wiki3.version = 1) AS author,
                string_agg(DISTINCT wiki.author, ', ') AS collaborators,
                TIMESTAMP WITH TIME ZONE 'epoch' + (MIN(wiki.time)/1000000) * INTERVAL '1s' AS created,
                TIMESTAMP WITH TIME ZONE 'epoch' + (MAX(wiki.time)/1000000) * INTERVAL '1s' AS modified
            FROM wiki
            GROUP BY wiki.name;
        ''')

    def backwards(self, orm):
        # Selecting trac database
        connection = connections['trac']

        cursor = connection.cursor()

        cursor.execute('''
            CREATE OR REPLACE VIEW wiki_view AS SELECT
                wiki.name AS name,
                (SELECT wiki2.text FROM wiki AS wiki2 WHERE wiki2.name = wiki.name
                 AND wiki2.version = MAX(wiki.version)) AS wiki_text,
                (SELECT wiki3.author FROM wiki AS wiki3 WHERE wiki3.name = wiki.name
                 AND wiki3.version = 1) AS author,
                string_agg(DISTINCT wiki.author, ', ') AS collaborators,
                TIMESTAMP WITH TIME ZONE 'epoch' + (MAX(wiki.time)/1000000) * INTERVAL '1s' AS created,
                TIMESTAMP WITH TIME ZONE 'epoch' + (MIN(wiki.time)/1000000) * INTERVAL '1s' AS modified
            FROM wiki
            GROUP BY wiki.name;
        ''')

    models = {
        u'proxy.attachment': {
            'Meta': {'object_name': 'Attachment', 'db_table': "'attachment_view'", 'managed': 'False'},
            'attach_id': ('django.db.models.fields.TextField', [], {}),
            'author': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filename': ('django.db.models.fields.TextField', [], {}),
            'mimetype': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'used_by': ('django.db.models.fields.TextField', [], {})
        },
        u'proxy.revision': {
            'Meta': {'object_name': 'Revision', 'db_table': "'revision_view'", 'managed': 'False'},
            'author': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'repository_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rev': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
