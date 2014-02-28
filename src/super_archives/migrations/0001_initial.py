# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailAddressValidation'
        db.create_table(u'super_archives_emailaddressvalidation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emails_not_validated', null=True, to=orm['accounts.User'])),
            ('validation_key', self.gf('django.db.models.fields.CharField')(default='143df80aa814429f9938d3b165148480', max_length=32, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'super_archives', ['EmailAddressValidation'])

        # Adding unique constraint on 'EmailAddressValidation', fields ['user', 'address']
        db.create_unique(u'super_archives_emailaddressvalidation', ['user_id', 'address'])

        # Adding model 'EmailAddress'
        db.create_table(u'super_archives_emailaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emails', null=True, on_delete=models.SET_NULL, to=orm['accounts.User'])),
            ('address', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('real_name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64, blank=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
        ))
        db.send_create_signal(u'super_archives', ['EmailAddress'])

        # Adding model 'MailingList'
        db.create_table(u'super_archives_mailinglist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('logo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('last_imported_index', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'super_archives', ['MailingList'])

        # Adding model 'MailingListMembership'
        db.create_table(u'super_archives_mailinglistmembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('mailinglist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.MailingList'])),
        ))
        db.send_create_signal(u'super_archives', ['MailingListMembership'])

        # Adding model 'Keyword'
        db.create_table(u'super_archives_keyword', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length='128')),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.Thread'])),
        ))
        db.send_create_signal(u'super_archives', ['Keyword'])

        # Adding model 'Thread'
        db.create_table(u'super_archives_thread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject_token', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('mailinglist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.MailingList'])),
            ('latest_message', self.gf('django.db.models.fields.related.OneToOneField')(related_name='+', unique=True, null=True, to=orm['super_archives.Message'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('spam', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'super_archives', ['Thread'])

        # Adding unique constraint on 'Thread', fields ['subject_token', 'mailinglist']
        db.create_unique(u'super_archives_thread', ['subject_token', 'mailinglist_id'])

        # Adding model 'Vote'
        db.create_table(u'super_archives_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.Message'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'super_archives', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['user', 'message']
        db.create_unique(u'super_archives_vote', ['user_id', 'message_id'])

        # Adding model 'Message'
        db.create_table(u'super_archives_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.EmailAddress'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.Thread'], null=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=512, db_index=True)),
            ('subject_clean', self.gf('django.db.models.fields.CharField')(max_length=512, db_index=True)),
            ('body', self.gf('django.db.models.fields.TextField')(default='')),
            ('received_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('message_id', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('spam', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'super_archives', ['Message'])

        # Adding unique constraint on 'Message', fields ['thread', 'message_id']
        db.create_unique(u'super_archives_message', ['thread_id', 'message_id'])

        # Adding model 'MessageBlock'
        db.create_table(u'super_archives_messageblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='blocks', to=orm['super_archives.Message'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('is_reply', self.gf('django.db.models.fields.BooleanField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'super_archives', ['MessageBlock'])

        # Adding model 'MessageMetadata'
        db.create_table(u'super_archives_messagemetadata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['super_archives.Message'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'super_archives', ['MessageMetadata'])


    def backwards(self, orm):
        # Removing unique constraint on 'Message', fields ['thread', 'message_id']
        db.delete_unique(u'super_archives_message', ['thread_id', 'message_id'])

        # Removing unique constraint on 'Vote', fields ['user', 'message']
        db.delete_unique(u'super_archives_vote', ['user_id', 'message_id'])

        # Removing unique constraint on 'Thread', fields ['subject_token', 'mailinglist']
        db.delete_unique(u'super_archives_thread', ['subject_token', 'mailinglist_id'])

        # Removing unique constraint on 'EmailAddressValidation', fields ['user', 'address']
        db.delete_unique(u'super_archives_emailaddressvalidation', ['user_id', 'address'])

        # Deleting model 'EmailAddressValidation'
        db.delete_table(u'super_archives_emailaddressvalidation')

        # Deleting model 'EmailAddress'
        db.delete_table(u'super_archives_emailaddress')

        # Deleting model 'MailingList'
        db.delete_table(u'super_archives_mailinglist')

        # Deleting model 'MailingListMembership'
        db.delete_table(u'super_archives_mailinglistmembership')

        # Deleting model 'Keyword'
        db.delete_table(u'super_archives_keyword')

        # Deleting model 'Thread'
        db.delete_table(u'super_archives_thread')

        # Deleting model 'Vote'
        db.delete_table(u'super_archives_vote')

        # Deleting model 'Message'
        db.delete_table(u'super_archives_message')

        # Deleting model 'MessageBlock'
        db.delete_table(u'super_archives_messageblock')

        # Deleting model 'MessageMetadata'
        db.delete_table(u'super_archives_messagemetadata')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'github': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'google_talk': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'verification_hash': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'webpage': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
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
        },
        u'super_archives.emailaddress': {
            'Meta': {'ordering': "('id',)", 'object_name': 'EmailAddress'},
            'address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'real_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['accounts.User']"})
        },
        u'super_archives.emailaddressvalidation': {
            'Meta': {'unique_together': "(('user', 'address'),)", 'object_name': 'EmailAddressValidation'},
            'address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails_not_validated'", 'null': 'True', 'to': u"orm['accounts.User']"}),
            'validation_key': ('django.db.models.fields.CharField', [], {'default': "'aa4ac05f39464a05932308e9fda2daf5'", 'max_length': '32', 'null': 'True'})
        },
        u'super_archives.keyword': {
            'Meta': {'ordering': "('?',)", 'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': "'128'"}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.Thread']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'super_archives.mailinglist': {
            'Meta': {'object_name': 'MailingList'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_imported_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'logo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'super_archives.mailinglistmembership': {
            'Meta': {'object_name': 'MailingListMembership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.MailingList']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        },
        u'super_archives.message': {
            'Meta': {'ordering': "('received_time',)", 'unique_together': "(('thread', 'message_id'),)", 'object_name': 'Message'},
            'body': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'from_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.EmailAddress']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'received_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'spam': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512', 'db_index': 'True'}),
            'subject_clean': ('django.db.models.fields.CharField', [], {'max_length': '512', 'db_index': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.Thread']", 'null': 'True'})
        },
        u'super_archives.messageblock': {
            'Meta': {'ordering': "('order',)", 'object_name': 'MessageBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_reply': ('django.db.models.fields.BooleanField', [], {}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blocks'", 'to': u"orm['super_archives.Message']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'super_archives.messagemetadata': {
            'Message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.Message']"}),
            'Meta': {'object_name': 'MessageMetadata'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'super_archives.thread': {
            'Meta': {'ordering': "('-latest_message__received_time',)", 'unique_together': "(('subject_token', 'mailinglist'),)", 'object_name': 'Thread'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_message': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'null': 'True', 'to': u"orm['super_archives.Message']"}),
            'mailinglist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.MailingList']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'spam': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_token': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'super_archives.vote': {
            'Meta': {'unique_together': "(('user', 'message'),)", 'object_name': 'Vote'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['super_archives.Message']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        }
    }

    complete_apps = ['super_archives']