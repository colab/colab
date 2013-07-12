# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PageHit'
        db.create_table('super_archives_pagehit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url_path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2048, db_index=True)),
            ('hit_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('super_archives', ['PageHit'])

        # Adding model 'EmailAddress'
        db.create_table('super_archives_emailaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emails', null=True, to=orm['auth.User'])),
            ('address', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('real_name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
        ))
        db.send_create_signal('super_archives', ['EmailAddress'])

        # Adding model 'UserProfile'
        db.create_table('super_archives_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('google_talk', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('webpage', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('super_archives', ['UserProfile'])

        # Adding model 'MailingList'
        db.create_table('super_archives_mailinglist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('logo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('last_imported_index', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('super_archives', ['MailingList'])

        # Adding model 'MailingListMembership'
        db.create_table('super_archives_mailinglistmembership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('mailinglist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.MailingList'])),
        ))
        db.send_create_signal('super_archives', ['MailingListMembership'])

        # Adding model 'Thread'
        db.create_table('super_archives_thread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject_token', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('mailinglist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.MailingList'])),
            ('latest_message', self.gf('django.db.models.fields.related.OneToOneField')(related_name='+', unique=True, null=True, to=orm['super_archives.Message'])),
        ))
        db.send_create_signal('super_archives', ['Thread'])

        # Adding unique constraint on 'Thread', fields ['subject_token', 'mailinglist']
        db.create_unique('super_archives_thread', ['subject_token', 'mailinglist_id'])

        # Adding model 'Vote'
        db.create_table('super_archives_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.Message'])),
        ))
        db.send_create_signal('super_archives', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['user', 'message']
        db.create_unique('super_archives_vote', ['user_id', 'message_id'])

        # Adding model 'Message'
        db.create_table('super_archives_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.EmailAddress'])),
            ('mailinglist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.MailingList'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.Thread'], null=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('subject_clean', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('body', self.gf('django.db.models.fields.TextField')(default='')),
            ('received_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('message_id', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal('super_archives', ['Message'])

        # Adding model 'MessageMetadata'
        db.create_table('super_archives_messagemetadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.Message'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('super_archives', ['MessageMetadata'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Vote', fields ['user', 'message']
        db.delete_unique('super_archives_vote', ['user_id', 'message_id'])

        # Removing unique constraint on 'Thread', fields ['subject_token', 'mailinglist']
        db.delete_unique('super_archives_thread', ['subject_token', 'mailinglist_id'])

        # Deleting model 'PageHit'
        db.delete_table('super_archives_pagehit')

        # Deleting model 'EmailAddress'
        db.delete_table('super_archives_emailaddress')

        # Deleting model 'UserProfile'
        db.delete_table('super_archives_userprofile')

        # Deleting model 'MailingList'
        db.delete_table('super_archives_mailinglist')

        # Deleting model 'MailingListMembership'
        db.delete_table('super_archives_mailinglistmembership')

        # Deleting model 'Thread'
        db.delete_table('super_archives_thread')

        # Deleting model 'Vote'
        db.delete_table('super_archives_vote')

        # Deleting model 'Message'
        db.delete_table('super_archives_message')

        # Deleting model 'MessageMetadata'
        db.delete_table('super_archives_messagemetadata')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'super_archives.emailaddress': {
            'Meta': {'object_name': 'EmailAddress'},
            'address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'super_archives.mailinglist': {
            'Meta': {'object_name': 'MailingList'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_imported_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'super_archives.mailinglistmembership': {
            'Meta': {'object_name': 'MailingListMembership'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['super_archives.MailingList']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'super_archives.message': {
            'Meta': {'object_name': 'Message'},
            'body': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'from_address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['super_archives.EmailAddress']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['super_archives.MailingList']"}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'received_time': ('django.db.models.fields.DateTimeField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'subject_clean': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['super_archives.Thread']", 'null': 'True'})
        },
        'super_archives.messagemetadata': {
            'Message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['super_archives.Message']"}),
            'Meta': {'object_name': 'MessageMetadata'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'super_archives.pagehit': {
            'Meta': {'object_name': 'PageHit'},
            'hit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'})
        },
        'super_archives.thread': {
            'Meta': {'unique_together': "(('subject_token', 'mailinglist'),)", 'object_name': 'Thread'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_message': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': "orm['super_archives.Message']"}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['super_archives.MailingList']"}),
            'subject_token': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'super_archives.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'google_talk': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'webpage': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'super_archives.vote': {
            'Meta': {'unique_together': "(('user', 'message'),)", 'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['super_archives.Message']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['super_archives']
