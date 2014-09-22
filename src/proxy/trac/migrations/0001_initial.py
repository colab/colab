# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connections


def create_views(apps, schema_editor):
    connection = connections['trac']

    cursor = connection.cursor()

    # revision_view
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

    # attachment_view
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

    # wiki_view
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
        ''')

    # ticket_view
    cursor.execute('''
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

    # ticket_collab_count_view
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
        ''')

    # wiki_collab_count_view
    cursor.execute('''
        CREATE OR REPLACE VIEW wiki_collab_count_view AS
        SELECT author, count(*) from wiki GROUP BY author;
        ''')


def drop_views(apps, schema_editor):
    connection = connections['trac']

    cursor = connection.cursor()
    cursor.execute('''
        DROP VIEW IF EXISTS revision_view;
        DROP VIEW IF EXISTS ticket_view;
        DROP VIEW IF EXISTS wiki_view;
        DROP VIEW IF EXISTS ticket_collab_count_view;
        DROP VIEW IF EXISTS wiki_collab_count_view;
        DROP VIEW IF EXISTS attachment_view;
        ''')


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(code=create_views, reverse_code=drop_views)
    ]
