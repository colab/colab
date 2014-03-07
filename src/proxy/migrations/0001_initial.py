# -*- coding: utf-8 -*-
import datetime
from django.db import connections
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
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
                ticket.reporter as author,
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
        cursor.execute('''
CREATE OR REPLACE VIEW attachment_view AS SELECT
CONCAT(attachment.type, '/' , attachment.id, '/', attachment.filename) AS url,
attachment.type AS used_by,
attachment.filename AS filename,
attachment.id as attach_id,
(SELECT LOWER(SUBSTRING(attachment.filename FROM '\.(\w+)$'))) AS mimetype,
attachment.author AS author,
attachment.description AS description,
attachment.size AS size,
TIMESTAMP WITH TIME ZONE 'epoch' + (attachment.time/1000000)* INTERVAL '1s' AS created
FROM attachment;
''')
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
        cursor.execute('''
CREATE OR REPLACE VIEW wiki_view AS SELECT
wiki.name AS name,
(SELECT wiki2.text FROM wiki AS wiki2 WHERE wiki2.name = wiki.name
AND wiki2.version = MAX(wiki.version)) AS wiki_text,
(SELECT wiki3.author FROM wiki AS wiki3 WHERE wiki3.name = wiki.name
AND wiki3.version = 1) AS author,
string_agg(DISTINCT wiki.author, ', ') AS collaborators,
TIMESTAMP WITH TIME ZONE 'epoch' + (MIN(wiki.time)/1000000) * INTERVAL '1s' AS created,
TIMESTAMP WITH TIME ZONE 'epoch' + (MAX(wiki.time)/1000000) * INTERVAL '1s' AS modified,
(SELECT wiki4.author FROM wiki AS wiki4 WHERE wiki4.name = wiki.name
AND wiki4.version = MAX(wiki.version)) AS modified_by
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
ticket.reporter as author,
ticket.status as status,
ticket.keywords as keywords,
(SELECT
string_agg(DISTINCT ticket_change.author, ', ')
FROM ticket_change WHERE ticket_change.ticket = ticket.id
GROUP BY ticket_change.ticket) as collaborators,
TIMESTAMP WITH TIME ZONE 'epoch' + (time/1000000)* INTERVAL '1s' AS created,
TIMESTAMP WITH TIME ZONE 'epoch' + (changetime/1000000) * INTERVAL '1s' AS modified,
(SELECT
ticket_change.author
FROM ticket_change
WHERE ticket_change.ticket = ticket.id
AND ticket_change.time = ticket.changetime
LIMIT 1
) AS modified_by
FROM ticket;
''')
        cursor.execute('''
CREATE OR REPLACE VIEW ticket_collab_count_view AS
SELECT
COALESCE (t1.author, t2.author) as author,
(COALESCE(t1.count, 0) + COALESCE(t2.count, 0)) as count
FROM
(SELECT author, count(*) as count
FROM ticket_change
GROUP BY author
ORDER BY author
) AS t1
FULL OUTER JOIN
(SELECT reporter as author, count(*) as count
FROM ticket
GROUP BY reporter
ORDER BY reporter
) AS t2
ON t1.author = t2.author;

CREATE OR REPLACE VIEW wiki_collab_count_view AS
SELECT author, count(*) from wiki GROUP BY author;
''')

        pass

    def backwards(self, orm):
        connection = connections['trac']

        cursor = connection.cursor()
        cursor.execute('''
DROP VIEW IF EXISTS revision_view;
DROP VIEW IF EXISTS ticket_view;
DROP VIEW IF EXISTS wiki_view;
''')
	cursor.execute('DROP VIEW IF EXISTS attachment_view;')

    pass

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
            'modified_by': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'priority': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reporter': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'severity': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'proxy.ticketcollabcount': {
            'Meta': {'object_name': 'TicketCollabCount', 'db_table': "'ticket_collab_count_view'", 'managed': 'False'},
            'author': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {})
        },
        u'proxy.wiki': {
            'Meta': {'object_name': 'Wiki', 'db_table': "'wiki_view'", 'managed': 'False'},
            'author': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'collaborators': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'wiki_text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'proxy.wikicollabcount': {
            'Meta': {'object_name': 'WikiCollabCount', 'db_table': "'wiki_collab_count_view'", 'managed': 'False'},
            'author': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['proxy']
    symmetrical = True
