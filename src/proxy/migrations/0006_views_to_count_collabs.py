# -*- coding: utf-8 -*-
from django.db import connections
from south.v2 import DataMigration

class Migration(DataMigration):

    def forwards(self, orm):
        # Selecting trac database
        connection = connections['trac']

        cursor = connection.cursor()
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

    def backwards(self, orm):
        # Selecting trac database
        connection = connections['trac']

        cursor = connection.cursor()
        cursor.execute('''
            DROP VIEW ticket_collab_count_view;
            DROP VIEW wiki_collab_count_view;
        ''')

    complete_apps = ['proxy']
    symmetrical = True
