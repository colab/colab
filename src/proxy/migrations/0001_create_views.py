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
                TIMESTAMP WITH TIME ZONE 'epoch' + (MAX(wiki.time)/1000000) * INTERVAL '1s' AS created,
                TIMESTAMP WITH TIME ZONE 'epoch' + (MIN(wiki.time)/1000000) * INTERVAL '1s' AS modified
            FROM wiki
            GROUP BY wiki.name;

            CREATE OR REPLACE VIEW ticket_view AS SELECT
                ticket.id AS id,
                ticket.summary as summary,
                ticket.description as description,
                ticket.milestone as milestone,
                ticket.priority as priority,
                ticket.component as component,
                ticket.version as version,
                ticket.severity as severity,
                ticket.reporter as reporter,
                ticket.owner as author,
                ticket.status as status,
                ticket.keywords as keywords,
                (SELECT
                    string_agg(DISTINCT ticket_change.author, ', ')
                    FROM ticket_change WHERE ticket_change.ticket = ticket.id
                    GROUP BY ticket_change.ticket) as collaborators,
                TIMESTAMP WITH TIME ZONE 'epoch' + (time/1000000)* INTERVAL '1s' AS created,
                TIMESTAMP WITH TIME ZONE 'epoch' + (changetime/1000000) * INTERVAL '1s' AS modified
            FROM ticket;

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

    def backwards(self, orm):
        # Selecting trac database
        connection = connections['trac']

        cursor = connection.cursor()
        cursor.execute('''
            DROP VIEW IF EXISTS revision_view;
            DROP VIEW IF EXISTS ticket_view;
            DROP VIEW IF EXISTS wiki_view;
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
